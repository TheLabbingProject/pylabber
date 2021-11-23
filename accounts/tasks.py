"""
Celery tasks exposed by the :mod:`pylabber.accounts` app.
"""
import math
from pathlib import Path
from typing import Iterable, List, Union

from celery import group, shared_task
from django_mri.models import Scan, Session
from paramiko.ssh_exception import SSHException
from research.models.subject import Subject

from accounts.models.export_destination import ExportDestination


@shared_task(
    name="accounts.export-files",
    autoretry_for=(OSError, SSHException),
    retry_backoff=True,
)
def export_files(export_destination_id: int, files: List[str]):
    host = ExportDestination.objects.get(id=export_destination_id)
    host.put(files)


@shared_task(name="accounts.export-mri-scan",)
def export_mri_scan(
    export_destination_id: int,
    scan_id: int,
    file_format: Union[str, List[str]] = "DICOM",
    max_parallel: int = 3,
):
    """
    Exports a single MRI scan to the specified export destination.

    Parameters
    ----------
    export_destination_id : int
        Export destination ID
    scan_id : int
        Scan ID
    file_format : Union[str, List[str]]
        Either DICOM or NIfTI or both
    max_parallel : int
        Maximal number of parallel processes
    """
    # Split in case of multiple sessions.
    if isinstance(scan_id, Iterable):
        try:
            n_chunks = math.ceil(len(scan_id) / max_parallel)
        except ZeroDivisionError:
            # If `max_parallel` is set to 0, run all in parallel.
            signatures = [
                export_mri_scan.s(export_destination_id, pk, file_format)
                for pk in scan_id
            ]
            group(signatures)()
        else:
            # Create the inputs for each separate execution and run in chunks.
            inputs = (
                (export_destination_id, pk, file_format) for pk in scan_id
            )
            chunks = export_mri_scan.chunks(inputs, n_chunks)
            chunks.group().skew()()
        finally:
            return
    # Split in case of multiple export destinations.
    if isinstance(export_destination_id, Iterable):
        signatures = [
            export_mri_scan.s(pk, scan_id, file_format)
            for pk in export_destination_id
        ]
        group(signatures)()
        return
    # Split in case of multiple file formats.
    if isinstance(file_format, list):
        # Fix list passed as a single string.
        if len(file_format) == 1:
            file_format = file_format.pop().split(",")
        signatures = [
            export_mri_scan.s(export_destination_id, scan_id, f)
            for f in file_format
        ]
        group(signatures)()
        return
    elif isinstance(file_format, str):
        file_format = file_format.split(",")
        if len(file_format) > 1:
            export_mri_scan.delay(export_destination_id, scan_id, file_format)
            return
        else:
            file_format = file_format.pop()
    file_format = file_format.lower()
    # Create an iterable of file paths.
    scan = Scan.objects.get(id=scan_id)
    files = []
    if file_format == "dicom":
        files = list(scan.dicom.image_set.values_list("dcm", flat=True))
    elif file_format == "nifti":
        nii_files = scan.nifti.get_file_paths()
        files += [str(path) for path in nii_files]
    export_files.delay(export_destination_id, files)


@shared_task(name="accounts.export-mri-session")
def export_mri_session(
    export_destination_id: int,
    session_id: int,
    file_format: Union[str, List[str]] = "DICOM",
    max_parallel: int = 3,
    max_parallel_scans: int = 3,
    skew: bool = True,
):
    """
    Export a single session's DICOM images to some remote location.

    Parameters
    ----------
    export_destination_id : int
        Export destination ID
    session_id : int
        Session ID
    file_format : Union[str, List[str]]
        Either DICOM or NIfTI or both
    max_parallel : int
        Maximal number of parallel processes
    """
    # Split in case of multiple sessions.
    if isinstance(session_id, Iterable):
        try:
            n_chunks = math.ceil(len(session_id) / max_parallel)
        except ZeroDivisionError:
            # If `max_parallel` is set to 0, run all in parallel.
            signatures = [
                export_mri_session.s(
                    export_destination_id,
                    pk,
                    file_format=file_format,
                    max_parallel_scans=max_parallel_scans,
                )
                for pk in session_id
            ]
            group(signatures)()
        else:
            # Create the inputs for each separate execution and run in chunks.
            inputs = (
                (
                    export_destination_id,
                    pk,
                    file_format,
                    max_parallel,
                    max_parallel_scans,
                )
                for pk in session_id
            )
            chunks = export_mri_session.chunks(inputs, n_chunks)
            grouped = chunks.group()
            if skew:
                grouped.skew()()
            else:
                grouped()
        finally:
            return
    # Split in case of multiple export destinations.
    if isinstance(export_destination_id, Iterable):
        signatures = [
            export_mri_session.s(
                pk,
                session_id,
                file_format=file_format,
                max_parallel=max_parallel,
                max_parallel_scans=max_parallel_scans,
                skew=skew,
            )
            for pk in export_destination_id
        ]
        group(signatures)()
        return
    # Split in case of multiple file formats.
    if isinstance(file_format, list):
        # Fix list passed as a single string.
        if len(file_format) == 1:
            file_format = file_format.pop().split(",")
        signatures = [
            export_mri_session.s(
                export_destination_id,
                session_id,
                file_format=f,
                max_parallel=max_parallel,
                max_parallel_scans=max_parallel_scans,
                skew=skew,
            )
            for f in file_format
        ]
        group(signatures)()
        return
    elif isinstance(file_format, str):
        file_format = file_format.split(",")
        if len(file_format) > 1:
            export_mri_session.delay(
                export_destination_id,
                session_id,
                file_format=file_format,
                max_parallel=max_parallel,
                max_parallel_scans=max_parallel_scans,
                skew=skew,
            )
            return
        else:
            file_format = file_format.pop()
    file_format = file_format.lower()
    # Create an iterable of file paths.
    session = Session.objects.get(id=session_id)
    scan_ids = session.scan_set.values_list("id", flat=True)
    export_mri_scan.delay(
        export_destination_id,
        list(scan_ids),
        file_format=file_format,
        max_parallel=max_parallel_scans,
    )


@shared_task(name="accounts.export-subject-mri-data")
def export_subject_mri_data(
    export_destination_id: int,
    subject_id: int,
    file_format: Union[str, List[str]] = "DICOM",
    max_parallel: int = 3,
    max_parallel_sessions: int = 3,
    max_parallel_scans: int = 3,
    skew: bool = True,
):
    """
    Export a single subject's MRI data to some remote location.

    Parameters
    ----------
    export_destination_id : int
        Export destination ID
    subject_id : int
        Subject ID
    file_format : Union[str, List[str]]
        Either DICOM or NIfTI or both
    max_parallel : int
        Maximal number of parallel processes
    """
    if isinstance(subject_id, Iterable):
        try:
            n_chunks = math.ceil(len(subject_id) / max_parallel)
        except ZeroDivisionError:
            # If `max_parallel` is set to 0, run all in parallel.
            signatures = [
                export_subject_mri_data.s(
                    export_destination_id,
                    pk,
                    file_format=file_format,
                    max_parallel_sessions=max_parallel_sessions,
                    max_parallel_scans=max_parallel_scans,
                    skew=skew,
                )
                for pk in subject_id
            ]
            group(signatures)()
        else:
            # Create the inputs for each separate execution and run in chunks.
            inputs = (
                (
                    export_destination_id,
                    pk,
                    file_format,
                    max_parallel,
                    max_parallel_sessions,
                    max_parallel_scans,
                    skew,
                )
                for pk in subject_id
            )
            chunks = export_subject_mri_data.chunks(inputs, n_chunks)
            grouped = chunks.group()
            if skew:
                grouped.skew()()
            grouped()
    else:
        subject = Subject.objects.get(id=subject_id)
        sessions_ids = list(
            subject.mri_session_set.values_list("id", flat=True)
        )
        export_mri_session.delay(
            export_destination_id,
            sessions_ids,
            file_format=file_format,
            max_parallel=max_parallel_sessions,
            max_parallel_scans=max_parallel_scans,
            skew=skew,
        )

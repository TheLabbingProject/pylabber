"""
Celery tasks exposed by the :mod:`pylabber.accounts` app.
"""
from typing import Dict

from celery import group, shared_task
from django_mri.models import Session
from research.models.subject import Subject

from accounts.models.export_destination import ExportDestination


@shared_task(name="accounts.export-mri-session")
def export_mri_session(
    export_destination_id: int,
    session_id: int,
    file_format: str = "DICOM",
    include_json: bool = True,
):
    """
    Export a single session's DICOM images to some remote location.

    Parameters
    ----------
    session_id : int
        Session ID
    export_destination_id : int
        Export destination ID
    file_format : str
        Either DICOM or NIfTI
    include_json : bool
        If exporting NIfTI files, whether to include the JSON sidecar or not
    """
    if isinstance(include_json, list):
        include_json = include_json.pop()
    if isinstance(file_format, list):
        if len(file_format) == 1:
            file_format = file_format.pop().split(",")
        signatures = [
            export_mri_session.s(
                export_destination_id, session_id, f, include_json
            )
            for f in file_format
        ]
        return group(signatures)()
    elif isinstance(file_format, str):
        file_format = file_format.split(",")
        if len(file_format) > 1:
            return export_mri_session(
                export_destination_id, session_id, file_format, include_json
            )
        else:
            file_format = file_format.pop()
    file_format = file_format.lower()
    # Create an iterable of file paths.
    session = Session.objects.get(id=session_id)
    files = []
    if file_format == "dicom":
        files = session.list_dicom_files()
    elif file_format == "nifti":
        files = session.list_nifti_files(include_json=include_json)

    # Find the remote location's definition in the database.
    host = ExportDestination.objects.get(id=export_destination_id)

    # Create the files and directories remotely.
    host.put(files)


@shared_task(name="accounts.export-subject-data")
def export_subject_data(subject_id: int, export_destination_id: int):
    # Create an iterable of DICOM image file paths.
    subject = Subject.objects.get(id=subject_id)
    files = subject.mri_session_set.values_list(
        "scan__dicom__image__dcm", flat=True
    )

    # Find the remote location's definition in the database.
    host = ExportDestination.objects.get(id=export_destination_id)

    host.put(files)

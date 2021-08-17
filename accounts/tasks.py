"""
Celery tasks exposed by the :mod:`pylabber.accounts` app.
"""
from celery import shared_task
from django_mri.models import Session
from research.models.subject import Subject

from accounts.models.export_destination import ExportDestination


@shared_task(name="accounts.export-mri-session")
def export_mri_session(session_id: int, export_destination_id: int):
    """
    Export a single session's DICOM images to some remote location.

    Parameters
    ----------
    session_id : int
        Session ID
    export_destination_id : int
        Export destination ID
    """
    # Create an iterable of DICOM image file paths.
    session = Session.objects.get(id=session_id)
    files = session.scan_set.values_list("dicom__image__dcm", flat=True)

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

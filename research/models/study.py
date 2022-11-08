"""
Definition of the :class:`Study` model.
"""
import shutil
from pathlib import Path
import tqdm
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from django_mri.utils import get_bids_dir, get_mri_root
from research.models.managers.study import StudyManager
from research.utils import get_subject_model

STUDY_IMAGE_UPLOAD_DESTINATION: str = "images/studies"
User = get_user_model()


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a single study in the database.
    """

    #: An optional image to supplement the description.
    image = models.ImageField(
        upload_to=STUDY_IMAGE_UPLOAD_DESTINATION, blank=True, null=True
    )

    #: Subjects associated with this study.
    #: This field is currently not used, but kept because in the future it
    #: might be used for "caching" associated subjects to save queries.
    subjects = models.ManyToManyField("research.Subject", blank=True)

    #: Researchers collaborating on this study.
    collaborators = models.ManyToManyField(User, blank=True)

    #: The experimental procedures associated with this study.
    procedures = models.ManyToManyField("research.Procedure", blank=True)

    objects = StudyManager.as_manager()

    class Meta:
        ordering = ("title",)
        verbose_name_plural = "Studies"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the canonical URL for this instance.

        References
        ----------
        * `get_absolute_url()`_

        .. _get_absolute_url():
           https://docs.djangoproject.com/en/3.0/ref/models/instances/#get-absolute-url

        Returns
        -------
        str
            URL
        """
        return reverse("research:study-detail", args=[str(self.id)])

    def query_associated_subjects(self) -> models.QuerySet:
        """
        Returns a queryset of subjects associated with this study.

        See Also
        --------
        * :func:`subject_set`

        Returns
        -------
        models.QuerySet
            Subjects associated with this study
        """
        Subject = get_subject_model()
        return Subject.objects.filter(
            mri_session_set__scan__study_groups__study=self.id
        ).distinct()

    def get_data_directory(self) -> Path:
        return get_mri_root() / "studies" / str(self.id)

    def initiate_bids_directory(self):
        """
        Initiate the BIDS directory with all mandatory files.
        """
        self.bids_manager.set_description_json()
        self.bids_manager.generate_bidsignore()
        self.bids_manager.generate_readme()

    def create_data_directory(self, force: bool = False):
        Scan = apps.get_model("django_mri", "scan")
        BIDS_ROOT = get_bids_dir()
        if force and self.data_directory.exists():
            shutil.rmtree(self.data_directory)
        self.initiate_bids_directory()
        scans = Scan.objects.filter(study_groups__in=self.group_set.all())
        for scan in tqdm.tqdm(scans):
            try:
                if scan.nifti is None:
                    continue
            except FileNotFoundError:
                print(
                        f"WARNING! {scan} does not exist, skipping!"  # noqa: E501
                    )
                continue
            self.bids_manager.set_participant_tsv_and_json(scan)
            paths = scan.nifti.get_file_paths()
            for path in paths:
                try:
                    link_path = self.data_directory / path.relative_to(BIDS_ROOT)
                except ValueError:
                    print(
                        f"WARNING! {scan} does not have a BIDS compatible destination, skipping!"  # noqa: E501
                    )
                if link_path.exists():
                    continue
                link_path.parent.mkdir(parents=True, exist_ok=True)
                link_path.symlink_to(path)

    @property
    def data_directory(self) -> Path:
        return self.get_data_directory()

    @property
    def bids_manager(self):
        from django_mri.utils.bids import BidsManager

        return BidsManager(bids_dir=self.data_directory)

    @property
    def subject_set(self) -> models.QuerySet:
        """
        Returns a queryset of subjects associated with this study.

        See Also
        --------
        * :func:`query_associated_subjects`

        Returns
        -------
        models.QuerySet
            Subjects associated with this study
        """
        return self.query_associated_subjects()

    @property
    def n_subjects(self) -> int:
        """
        Returns the number of subjects associated with this study.

        Returns
        -------
        int
            Number of subjects associated with this study
        """
        return self.subject_set.count()

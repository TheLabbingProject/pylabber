"""
Definition of the :class:`Study` model.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
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
        mri_session_subjects = self.procedures.values_list(
            "events__measurementdefinition__mri_session_set__subject",
            flat=True,
        ).distinct()
        mri_scan_subjects = self.group_set.values_list(
            "mri_scan_set__session__subject", flat=True
        ).distinct()
        subject_ids = set(list(mri_session_subjects) + list(mri_scan_subjects))
        return Subject.objects.filter(id__in=subject_ids)

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

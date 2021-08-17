"""
Definition of the :class:`Study` model.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from research.models.managers.study import StudyManager
from research.utils import get_subject_model


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a single study in the database.
    """

    #: An optional image to supplement the description.
    image = models.ImageField(
        upload_to="images/studies", blank=True, null=True
    )

    #: Subjects associated with this study.
    #: This field is currently not used, but kept because in the future it
    #: might be used for "caching" associated subjects to save queries.
    subjects = models.ManyToManyField("research.Subject", blank=True)

    #: Researchers collaborating on this study.
    collaborators = models.ManyToManyField(get_user_model(), blank=True)

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

    def query_associated_subjects(
        self, id_only: bool = False
    ) -> models.QuerySet:
        Subject = get_subject_model()
        subject_ids = [
            subject.id
            for subject in Subject.objects.all()
            if self.id in subject.query_studies(id_only=True)
        ]
        return (
            subject_ids
            if id_only
            else Subject.objects.filter(id__in=subject_ids)
        )

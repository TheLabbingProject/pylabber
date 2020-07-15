"""
Definition of the :class:`~research.models.study.Study` model.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .subject import Subject


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a single study in the database.
    """

    #: An optional image to supplement the description.
    image = models.ImageField(
        upload_to="images/studies", blank=True, null=True
    )

    #: Subjects associated with this study.
    subjects = models.ManyToManyField(Subject, blank=True)

    #: Researchers collaborating on this study.
    collaborators = models.ManyToManyField(get_user_model(), blank=True)

    class Meta:
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

        return reverse("research:study_detail", args=[str(self.id)])

"""
Definition of the :class:`~accounts.models.laboratory.Laboratory` model.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Laboratory(TitleDescriptionModel, TimeStampedModel):
    """
    A class to represents a research laboratory.
    """

    image = models.ImageField(upload_to="images/labs", blank=True, null=True)
    members = models.ManyToManyField(
        get_user_model(), blank=True, through="accounts.LaboratoryMembership"
    )

    class Meta:
        verbose_name_plural = "Laboratories"
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return self.title

    def get_absolute_url(self) -> str:
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

        return reverse("research:laboratory-detail", args=[str(self.id)])


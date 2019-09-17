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

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("research:laboratory_detail", args=[str(self.id)])


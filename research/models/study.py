from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .subject import Subject


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    A model to represent a single study. Has a ManyToMany relationship
    with both :class:`research.Subject` and :class:`accounts.User`.

    """

    image = models.ImageField(upload_to="images/studies", blank=True, null=True)

    subjects = models.ManyToManyField(Subject, blank=True)
    collaborators = models.ManyToManyField(get_user_model(), blank=True)

    class Meta:
        verbose_name_plural = "Studies"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("research:study_detail", args=[str(self.id)])

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .subject import Subject


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    Stores a single study. Each study may has a ManyToMany relationship
    with both :model:`research.Subject` and :model:`accounts.User`.

    """

    image = models.ImageField(upload_to="images/studies", blank=True)

    subjects = models.ManyToManyField(Subject)
    collaborators = models.ManyToManyField(get_user_model())

    class Meta:
        verbose_name_plural = "Studies"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("research:study_detail", args=[str(self.id)])

    def generate_dicom_tree(self) -> list:
        """
        Returns a list of dictionairies meant to be passed to jstree for
        presentation in the template. Probably should be replaced with a
        serializer once a RESTful API is set-up.
        
        Returns
        -------
        list
            A list of dictionaries representing jstree nodes.
        """

        return [subject.to_tree() for subject in self.subjects.all()]

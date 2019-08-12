from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Group(TitleDescriptionModel, TimeStampedModel):
    study = models.ForeignKey("research.Study", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("study", "title")

    def __str__(self) -> str:
        return f"{self.study.title}|{self.title}"


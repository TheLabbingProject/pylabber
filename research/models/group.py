"""
Definition of the :class:`~research.models.group.Group` model.
"""

from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Group(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a unique study group (i.e. a grouping of subjects according to
    some experimental design in the context of a study).
    """

    #: The study associated with this experimental group.
    study = models.ForeignKey("research.Study", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("study", "title")

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return f"{self.study.title}|{self.title}"


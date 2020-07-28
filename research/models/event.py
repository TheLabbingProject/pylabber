"""
Definition of the :class:`~research.models.event.Event` model.
"""

from django_extensions.db.models import TitleDescriptionModel
from model_utils.managers import InheritanceManager


class Event(TitleDescriptionModel):
    """
    Represents an event as a part of a procedure.
    """

    objects = InheritanceManager()

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return f"{self.title}|{self.description}"

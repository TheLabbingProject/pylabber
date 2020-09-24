"""
Definition of the :class:`~research.models.ListItem`
"""
from django.db import models


class ListItem(models.Model):
    """
    Represents an item in the :class:`~research.models.Event` list of :class:`~research.models.Procedure` model.
    """

    index = models.PositiveIntegerField()
    event = models.ForeignKey("research.Event", on_delete=models.CASCADE)

    class Meta:
        ordering = ("index",)

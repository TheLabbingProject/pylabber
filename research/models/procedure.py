"""
Definition of the :class:`~research.models.Procedure` model.
"""

from django.db import models
from research.models.event import Event


class Procedure(models.Model):
    """
    Represents a procedure.
    """

    events = models.ManyToManyField(Event, through="ListItem")

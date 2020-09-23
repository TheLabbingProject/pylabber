"""
Definition of the :class:`~research.models.MeasurementDefinition` model.
"""

from django.db import models
from research.models.event import Event


class MeasurementDefinition(Event):
    """
    Represents an experimental measurement definition.
    """

    pass


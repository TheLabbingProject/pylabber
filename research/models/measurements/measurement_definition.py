"""
Definition of the :class:`~research.models.measurements.MeasurementDefinition` model.
"""

from django.db import models
from research.models.event import Event
from research.utils.utils import get_measurement_model


class MeasurementDefinition(Event):
    """
    Represents an experimental measurement definition.
    """


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

    measurement = models.ForeignKey(
        get_measurement_model(),
        on_delete=models.PROTECT,
        related_name="measurements",
        blank=True,
        null=True,
    )


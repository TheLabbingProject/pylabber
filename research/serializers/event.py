"""
Definition of the :class:`EventSerializer` class.
"""

from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from research.models.event import Event
from research.models.event_types import EventTypes
from research.serializers.measurement_definition import (
    MeasurementDefinitionSerializer,
)
from research.serializers.task import TaskSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer


SERIALIZERS = {
    EventTypes.MEASUREMENT.value: MeasurementDefinitionSerializer,
    EventTypes.TASK.value: TaskSerializer,
}


class BaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "id", "title", "description"


class EventSerializer(PolymorphicSerializer):
    """
    PolymorphicSerializer for the :class:`~research.models.event.Event`
    model.
    """

    class Meta:
        model = Event
        fields = "id", "title", "description"

    def get_serializer(self, input_type: str) -> Serializer:
        try:
            return SERIALIZERS.get(input_type, BaseEventSerializer)
        except KeyError:
            raise ValueError(f'Serializer for "{input_type}" does not exist')

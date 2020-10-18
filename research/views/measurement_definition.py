from pylabber.views.defaults import DefaultsMixin
from research.models.measurement_definition import MeasurementDefinition
from research.serializers.measurement_definition import (
    MeasurementDefinitionSerializer,
)
from rest_framework import viewsets


class MeasurementDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.measurement_definition.MeasurementDefinition` instances to
    be viewed or edited.

    """

    queryset = MeasurementDefinition.objects.order_by("title").all()
    serializer_class = MeasurementDefinitionSerializer

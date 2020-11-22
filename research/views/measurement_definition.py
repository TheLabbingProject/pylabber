from pylabber.views.defaults import DefaultsMixin
from research.filters.measurement_definition_filter import (
    MeasurementDefinitionFilter,
)
from research.models.measurement_definition import MeasurementDefinition
from research.serializers.measurement_definition import (
    MeasurementDefinitionSerializer,
    MeasurementDefinitionItemsSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer


class MeasurementDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.measurement_definition.MeasurementDefinition` instances to
    be viewed or edited.

    """

    filter_class = MeasurementDefinitionFilter
    queryset = MeasurementDefinition.objects.order_by("title").all()
    serializer_class = MeasurementDefinitionSerializer

    def get_serializer_class(self) -> Serializer:
        if self.action == "get_items":
            return MeasurementDefinitionItemsSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def get_items(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

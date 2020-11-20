from pylabber.views.defaults import DefaultsMixin
from research.filters.procedure_filter import ProcedureFilter
from research.models.procedure import Procedure
from research.serializers.procedure import (
    ProcedureSerializer,
    ProcedureItemsSerializer,
)
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProcedureViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.procedure.Procedure`
    instances to be viewed or edited.

    """

    filter_class = ProcedureFilter
    queryset = Procedure.objects.order_by("title").all()
    serializer_class = ProcedureSerializer

    def get_serializer_class(self) -> serializers.Serializer:
        if self.action == "get_items":
            return ProcedureItemsSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def get_items(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

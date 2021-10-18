"""
Definition of the :class:`ProcedureViewSet` class.
"""
from pylabber.views.defaults import DefaultsMixin
from research.filters.procedure_filter import ProcedureFilter
from research.models.procedure import Procedure
from research.serializers.procedure import ProcedureSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class ProcedureViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.procedure.Procedure`
    instances to be viewed or edited.
    """

    filter_class = ProcedureFilter
    queryset = Procedure.objects.order_by("title").all()
    serializer_class = ProcedureSerializer

    @action(detail=False, methods=["get"])
    def get_items(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

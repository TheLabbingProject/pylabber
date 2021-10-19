"""
Definition of the :class:`ProcedureStepViewSet` class.
"""
from pylabber.views.defaults import DefaultsMixin
from research.filters.procedure_step_filter import ProcedureStepFilter
from research.models.procedure_step import ProcedureStep
from research.serializers.procedure_step import ProcedureStepSerializer
from rest_framework import viewsets


class ProcedureStepViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows
    :class:`~research.models.procedure_step.ProcedureStep` instances to be
    viewed or edited.
    """

    filter_class = ProcedureStepFilter
    queryset = ProcedureStep.objects.all()
    serializer_class = ProcedureStepSerializer

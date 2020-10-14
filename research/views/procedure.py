from pylabber.views.defaults import DefaultsMixin
from research.models.procedure import Procedure
from research.serializers.procedure import ProcedureSerializer
from rest_framework import viewsets


class ProcedureViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.procedure.Procedure` instances to
    be viewed or edited.

    """

    queryset = Procedure.objects.order_by("title").all()
    serializer_class = ProcedureSerializer

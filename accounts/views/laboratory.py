from accounts.models.laboratory import Laboratory
from accounts.serializers.laboratory import LaboratorySerializer
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class LaboratoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.laboratory.Laboratory` instances
    to be viewed or edited.
    
    """

    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer


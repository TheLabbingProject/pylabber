from accounts.models.laboratory import Laboratory
from accounts.serializers.laboratory import LaboratorySerializer
from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class LaboratoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows studies to be viewed or edited.
    
    """

    pagination_class = StandardResultsSetPagination
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer


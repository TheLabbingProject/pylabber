from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from research.models.study import Study
from research.serializers.study import StudySerializer
from rest_framework import viewsets


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows studies to be viewed or edited.
    
    """

    pagination_class = StandardResultsSetPagination
    queryset = Study.objects.all()
    serializer_class = StudySerializer

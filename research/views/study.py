"""
Definition of the :class:`StudyViewSet` class.
"""
from pylabber.views.defaults import DefaultsMixin
from research.filters.study_filter import StudyFilter
from research.models.study import Study
from research.serializers.study import StudySerializer
from rest_framework import viewsets
from rest_framework.request import Request


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.study.Study` instances to
    be viewed or edited.
    """

    filter_class = StudyFilter
    queryset = Study.objects.order_by("title").all()
    serializer_class = StudySerializer

    def put(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

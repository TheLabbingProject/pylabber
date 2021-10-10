"""
Definintion of the :class:`StudyViewSet` class.
"""
from pylabber.views.defaults import DefaultsMixin
from research.filters.study_filter import StudyFilter
from research.models.study import Study
from research.serializers.study import StudySerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from research.views.utils import STUDY_AGGREGATIONS


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.study.Study` instances to
    be viewed or edited.
    """

    filter_class = StudyFilter
    queryset = Study.objects.with_counts().order_by("title")
    serializer_class = StudySerializer

    def filter_queryset(self, queryset):
        """
        Filters the returned study queryset according to the user's
        collaborations.

        Parameters
        ----------
        queryset : QuerySet
            Base `Study` queryset

        Returns
        -------
        QuerySet
            Studies in which the user is a collaborator
        """
        user = self.request.user
        if user.is_superuser:
            return super().filter_queryset(queryset)
        return queryset.filter(collaborators__in=[user])

    @action(detail=False, methods=["get"])
    def aggregate(self, request) -> Response:
        result = self.queryset.aggregate(**STUDY_AGGREGATIONS)
        return Response(result)

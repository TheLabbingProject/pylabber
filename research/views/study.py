"""
Definition of the :class:`StudyViewSet` class.
"""
from typing import Tuple

from django.db.models import QuerySet
from pylabber.utils.configuration import ENABLE_COUNT_FILTERING
from pylabber.views.defaults import DefaultsMixin
from research.filters.study_filter import StudyFilter
from research.models.study import Study
from research.serializers.study import StudySerializer
from research.views.messages import COUNT_FILTERING_DISABLED
from research.views.utils import STUDY_AGGREGATIONS
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

DEFAULT_STUDY_ORDERING: Tuple[str] = ("title",)


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.study.Study` instances to
    be viewed or edited.
    """

    filter_class = StudyFilter
    queryset = Study.objects.order_by(*DEFAULT_STUDY_ORDERING)
    serializer_class = StudySerializer

    def get_queryset(self) -> QuerySet:
        """
        Overrides the parent :func:`get_queryset` method to apply aggregated
        annotation if count filtering is enabled.

        Returns
        -------
        QuerySet
            Patient queryset
        """
        queryset = super().get_queryset()
        return queryset.with_counts() if ENABLE_COUNT_FILTERING else queryset

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
        return queryset.filter(collaborators=user)

    @action(detail=False, methods=["get"])
    def aggregate(self, request) -> Response:
        """
        Returns related model counts if count filtering is enabled.

        Parameters
        ----------
        request : Request
            API request

        Returns
        -------
        Response
            Aggregated queryset or informational message
        """
        queryset = self.filter_queryset(self.get_queryset())
        if ENABLE_COUNT_FILTERING:
            result = queryset.aggregate(**STUDY_AGGREGATIONS)
        else:
            result = COUNT_FILTERING_DISABLED
        return Response(result)

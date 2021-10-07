"""
Definition of the :class:`TaskResultViewSet` class.
"""
from typing import Tuple

from accounts.filters.task_result import TaskResultFilter
from accounts.serializers.task_result import TaskResultSerializer
from django_celery_results.models import TaskResult
from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets

TASK_ORDERING_FIELDS: Tuple[str] = (
    "status",
    "task_id",
    "task_name",
    "worker",
    "date_created",
    "date_done",
)


class TaskResultViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~django_celery_results.models.TaskResult`
    instances to be viewed or edited.
    """

    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_class = TaskResultFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = TASK_ORDERING_FIELDS

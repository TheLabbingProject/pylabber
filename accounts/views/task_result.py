"""
Definition of the :class:`TaskResultViewSet` class.
"""
from accounts.filters.task_result import TaskResultFilter
from accounts.serializers.task_result import TaskResultSerializer
from django_celery_results.models import TaskResult
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class TaskResultViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~django_celery_results.models.TaskResult`
    instances to be viewed or edited.
    """

    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_class = TaskResultFilter

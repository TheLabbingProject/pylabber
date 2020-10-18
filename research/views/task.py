from pylabber.views.defaults import DefaultsMixin
from research.models.task import Task
from research.serializers.task import TaskSerializer
from rest_framework import viewsets


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.task.Task` instances to
    be viewed or edited.

    """

    queryset = Task.objects.order_by("title").all()
    serializer_class = TaskSerializer

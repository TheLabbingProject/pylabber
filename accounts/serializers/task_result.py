"""
Definition of the :class:`TaskResultSerializer` class.
"""
import json

from django_celery_results.models import TaskResult
from rest_framework import serializers


class TaskResultSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_celery_results.models.TaskResult`
    model.
    """

    task_args = serializers.SerializerMethodField()
    task_kwargs = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = TaskResult
        fields = (
            "id",
            "task_id",
            "task_name",
            "task_args",
            "task_kwargs",
            "status",
            "worker",
            "date_created",
            "date_done",
            "result",
            "traceback",
            "meta",
        )

    def get_task_args(self, task):
        if task.task_args:
            return json.loads(task.task_args)

    def get_task_kwargs(self, task):
        if task.task_kwargs:
            return json.loads(task.task_kwargs)

    def get_meta(self, task):
        return json.loads(task.meta)

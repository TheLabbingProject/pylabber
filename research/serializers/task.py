"""
Definition of the :class:`~research.serializers.task.TaskSerializer` class.
"""

from research.models.task import Task
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.task.Task`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(view_name="research:task-detail")

    class Meta:
        model = Task
        fields = (
            "id",
            "url",
            "title",
            "description",
        )

"""
Definition of the :class:`ProcedureStepSerializer` class.
"""

from research.models.event import Event
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep
from research.serializers.event import EventSerializer
from rest_framework import serializers


class ProcedureStepSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.procedure_step.ProcedureStep` model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    index = serializers.IntegerField(allow_null=True)
    event_info = serializers.SerializerMethodField(source="event")
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    procedure = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all()
    )

    class Meta:
        model = ProcedureStep
        fields = (
            "id",
            "index",
            "event",
            "event_info",
            "procedure",
        )

    def get_event_info(self, instance):
        event = Event.objects.select_subclasses().get(id=instance.event.id)
        return EventSerializer(instance=event).data

"""
Definition of the :class:`ProcedureStepSerializer` class.
"""
from research.models.event import Event
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep
from research.serializers.event import EventSerializer
from rest_framework import serializers


class ProcedureStepSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for the
    :class:`~research.models.procedure_step.ProcedureStep` model.
    """

    procedure = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all()
    )
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    event_info = serializers.SerializerMethodField(source="event")
    index = serializers.IntegerField(allow_null=True)

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

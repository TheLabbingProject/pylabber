"""
Definition of the :class:`ProcedureStepSerializer` class.
"""

from research.models.event import Event
from research.models.procedure_step import ProcedureStep
from research.serializers.event import EventSerializer
from research.serializers.procedure import ProcedureSerializer
from rest_framework import serializers


class ProcedureStepSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.procedure_step.ProcedureStep` model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    event = serializers.SerializerMethodField()
    procedure = ProcedureSerializer(many=False)

    class Meta:
        model = ProcedureStep
        fields = "index", "event", "procedure"

    def get_event(self, instance):
        event = Event.objects.select_subclasses().get(id=instance.id)
        return EventSerializer(instance=event).data

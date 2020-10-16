"""
Definition of the :class:`ProcedureStepSerializer` class.
"""

from research.models.procedure_step import ProcedureStep
from research.serializers.event import EventSerializer
from research.serializers.procedure import ProcedureSerializer
from rest_framework import serializers


class ProcedureStepSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.procedure_step.ProcedureStep`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:procedure_step-detail"
    )

    event = EventSerializer(many=False)
    procedure = ProcedureSerializer(many=False)

    class Meta:
        model = ProcedureStep
        fields = ("index", "url", "event", "procedure")

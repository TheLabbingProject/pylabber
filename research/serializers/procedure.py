"""
Definition of the :class:`~research.serializers.procedure.ProcedureSerializer` class.
"""

from research.models.procedure import Procedure
from research.serializers.event import EventSerializer
from rest_framework import serializers


class ProcedureSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.procedure.Procedure`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:procedure-detail"
    )

    events = EventSerializer(many=True)

    class Meta:
        model = Procedure
        fields = ("id", "url", "title", "description", "events")

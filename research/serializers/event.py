"""
Definition of the :class:`~research.serializers.event.EventSerializer` class.
"""

from research.models.event import Event
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.event.Event`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:event-detail"
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "url",
            "title",
            "description",
        )

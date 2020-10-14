from pylabber.views.defaults import DefaultsMixin
from research.models.event import Event
from research.serializers.event import EventSerializer
from rest_framework import viewsets


class EventViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.event.Event` instances to
    be viewed or edited.

    """

    queryset = Event.objects.order_by("title").all()
    serializer_class = EventSerializer

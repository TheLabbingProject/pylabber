from pylabber.views.defaults import DefaultsMixin
from research.filters.event_filter import EventFilter
from research.models.event import Event
from research.serializers.event import EventSerializer
from rest_framework import viewsets


class EventViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.event.Event` instances to
    be viewed or edited.

    """

    filter_class = EventFilter
    queryset = Event.objects.select_subclasses()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.order_by("title").select_subclasses()

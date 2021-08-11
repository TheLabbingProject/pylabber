"""
Definition of the :class:`EventViewSet` class.
"""
from pylabber.views.defaults import DefaultsMixin
from research.filters.event_filter import EventFilter
from research.models.event import Event
from research.serializers.event import EventItemsSerializer, EventSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer


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

    def get_serializer_class(self) -> Serializer:
        if self.action == "get_items":
            return EventItemsSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def get_items(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

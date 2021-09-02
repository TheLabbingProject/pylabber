"""
Definition of the :class:`ExportDestinationViewSet` class.
"""
from accounts.filters import ExportDestinationFilter
from accounts.models.export_destination import ExportDestination
from accounts.serializers.export_destination import ExportDestinationSerializer
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class ExportDestinationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows
    :class:`~accounts.models.export_destination.ExportDestination` instances to
    be viewed or edited.
    """

    queryset = ExportDestination.objects.all()
    serializer_class = ExportDestinationSerializer
    filter_class = ExportDestinationFilter

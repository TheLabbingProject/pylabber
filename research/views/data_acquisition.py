"""
Definition of the :class:`DataAcquisitionViewSet` class.
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from pylabber.views.defaults import DefaultsMixin
from research.filters.data_acquisition_filter import DataAcquisitionFilter
from research.serializers.content_type import ContentTypeSerializer
from research.utils.data_acquisition_models import get_data_acquisition_models
from rest_framework import viewsets

DATA_ACQUISITION_MODELS = getattr(settings, "DATA_ACQUISITION_MODELS", set())


class DataAcquisitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that returns registered data acquisition models.
    """

    filter_class = DataAcquisitionFilter
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

    def get_queryset(self) -> QuerySet:
        """
        Returns only content types registered in the *DATA_ACQUISITION_MODELS*
        setting.

        Returns
        -------
        QuerySet
            Registered data acuisition models' content types
        """
        return get_data_acquisition_models()

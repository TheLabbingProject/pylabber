"""
Definition of the :class:`MeasurementDefinitionFilter` class.
"""
from django_filters import rest_framework as filters
from research.filters.event_filter import EventFilter
from research.filters.utils import LOOKUP_CHOICES
from research.models.measurement_definition import MeasurementDefinition


class MeasurementDefinitionFilter(EventFilter):
    """
    Provides useful filtering options for the
    :class:`~research.models.event.Event` model.
    """

    model_name = filters.CharFilter(
        field_name="content_type__model",
        lookup_expr="exact",
        label="Model name (exact)",
    )
    app_label = filters.CharFilter(
        field_name="content_type__app_label",
        lookup_expr="exact",
        label="App label (exact)",
    )

    class Meta:
        model = MeasurementDefinition
        fields = "id",

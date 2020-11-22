"""
Definition of the :class:`MeasurementDefinitionFilter` class.
"""

from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.measurement_definition import MeasurementDefinition


class MeasurementDefinitionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.event.Event` model.

    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)

    class Meta:
        model = MeasurementDefinition
        fields = "id", "title", "description"

"""
Definition of the :class:`EventFilter` class.
"""

from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.event import Event


class EventFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.event.Event` model.

    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    exclude_procedure = filters.NumberFilter(
        field_name="procedure", exclude=True
    )

    class Meta:
        model = Event
        fields = "id", "title", "description"

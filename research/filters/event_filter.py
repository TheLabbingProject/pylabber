"""
Definition of the :class:`EventFilter` class.
"""

from django_filters import rest_framework as filters
from research.models.event import Event


class EventFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.event.Event` model.

    """

    title = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    description = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )

    class Meta:
        model = Event
        fields = "id", "title", "description"

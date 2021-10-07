"""
Definition of the :class:`ExportDestinationFilter` class.
"""
from accounts.models.export_destination import ExportDestination
from django_filters import rest_framework as filters
from pylabber.utils.filters import DEFUALT_LOOKUP_CHOICES, NumberInFilter


class ExportDestinationFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~accounts.models.export_destination.ExportDestination` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    ip = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    username = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    destination = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    user_in = NumberInFilter(
        field_name="users__id", lookup_expr="in", label="User ID"
    )

    class Meta:
        model = ExportDestination
        fields = (
            "id",
            "title",
            "description",
            "ip",
            "username",
            "destination",
            "user_in",
        )

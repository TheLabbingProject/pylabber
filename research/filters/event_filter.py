"""
Definition of the :class:`EventFilter` class.
"""
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.event import Event
from research.models.procedure import Procedure
from research.models.study import Study


class EventFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.event.Event` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    procedure = filters.ModelMultipleChoiceFilter(
        queryset=Procedure.objects.all(), label="Procedures:"
    )
    exclude_procedure = filters.ModelMultipleChoiceFilter(
        queryset=Procedure.objects.all(),
        exclude=True,
        field_name="procedure",
        label="Exclude procedures:",
    )
    study = filters.ModelMultipleChoiceFilter(
        queryset=Study.objects.all(),
        label="Studies:",
        field_name="procedure__study",
    )

    class Meta:
        model = Event
        fields = ("id",)

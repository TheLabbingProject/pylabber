"""
Definition of the :class:`ProcedureStepFilter` class.
"""

from django_filters import rest_framework as filters
from research.models.procedure_step import ProcedureStep
from research.filters.utils import LOOKUP_CHOICES


class ProcedureStepFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.procedure_step.ProcedureStep` model.

    """

    title = filters.LookupChoiceFilter(
        field_name="event__title", lookup_choices=LOOKUP_CHOICES
    )
    description = filters.LookupChoiceFilter(
        field_name="event__description", lookup_choices=LOOKUP_CHOICES
    )

    class Meta:
        model = ProcedureStep
        fields = "id", "index", "procedure", "title", "description"

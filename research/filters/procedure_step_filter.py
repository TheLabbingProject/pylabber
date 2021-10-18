"""
Definition of the :class:`ProcedureStepFilter` class.
"""
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep


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
    exclude_procedure = filters.ModelMultipleChoiceFilter(
        field_name="procedure", exclude=True, queryset=Procedure.objects.all()
    )

    class Meta:
        model = ProcedureStep
        fields = (
            "id",
            "index",
            "procedure",
            "exclude_procedure",
            "title",
            "description",
        )

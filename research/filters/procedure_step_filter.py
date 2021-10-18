"""
Definition of the :class:`ProcedureStepFilter` class.
"""
from django.db.models import QuerySet
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep

EVENT_TYPE_QUERY_KEY: str = "event__{event_type}__isnull"


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
    event_type = filters.ChoiceFilter(
        choices=(
            ("measurementdefinition", "Measurement Definition"),
            ("task", "Task"),
        ),
        method="check_event_type",
        label="Event type:",
    )

    class Meta:
        model = ProcedureStep
        fields = (
            "id",
            "index",
            "procedure",
        )

    def check_event_type(
        self, queryset: QuerySet, name: str, value: str, *args, **kwargs
    ) -> QuerySet:
        key = EVENT_TYPE_QUERY_KEY.format(event_type=value)
        return queryset.filter(**{key: False})

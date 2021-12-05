"""
Definition of the :class:`ProcedureFilter` class.
"""
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.procedure import Procedure
from research.models.study import Study


class ProcedureFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.procedure.Procedure` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    study = filters.ModelMultipleChoiceFilter(queryset=Study.objects.all())
    exclude_study = filters.ModelMultipleChoiceFilter(
        field_name="study", exclude=True, queryset=Study.objects.all()
    )

    class Meta:
        model = Procedure
        fields = ("id",)

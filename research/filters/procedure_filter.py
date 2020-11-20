"""
Definition of the :class:`ProcedureFilter` class.
"""

from django_filters import rest_framework as filters
from research.models.procedure import Procedure
from research.models.study import Study


class ProcedureFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.procedure.Procedure` model.

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
    exclude_study = filters.ModelMultipleChoiceFilter(
        field_name="study", exclude=True, queryset=Study.objects.all()
    )

    class Meta:
        model = Procedure
        fields = "id", "title", "description", "study", "exclude_study"

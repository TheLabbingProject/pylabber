"""
Definition of the :class:`StudyFilter` class.
"""

from django_filters import rest_framework as filters
from research.models.study import Study


class StudyFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.study.Study` model.

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
        model = Study
        fields = (
            "id",
            "title",
            "description",
        )

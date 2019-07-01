from research.models.subject import Subject
from django_filters import rest_framework as filters


class SubjectFilter(filters.FilterSet):
    """
    Provides useful filtering options for the :class:`~research.models.subject.Subject`
    class.
    
    """

    born_after_date = filters.DateFilter("date_of_birth", lookup_expr="gte")
    born_before_date = filters.DateFilter("date_of_birth", lookup_expr="lte")
    first_name = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    last_name = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )

    class Meta:
        model = Subject
        fields = (
            "id",
            "first_name",
            "last_name",
            "sex",
            "gender",
            "born_after_date",
            "born_before_date",
            "dominant_hand",
        )

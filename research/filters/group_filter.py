from django_filters import rest_framework as filters
from research.models.group import Group
from research.models.study import Study


class GroupFilter(filters.FilterSet):
    """
    Provides useful filtering options for the :class:`~research.models.subject.Subject`
    model.
    
    """

    description = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    study = filters.ModelChoiceFilter(queryset=Study.objects.all())

    class Meta:
        model = Group
        fields = ("id", "title", "description")


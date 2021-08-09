"""
Definition of the :class:`GroupFilter` class.
"""
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.group import Group
from research.models.study import Study


class GroupFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.subject.Subject` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    study = filters.ModelChoiceFilter(queryset=Study.objects.all())

    class Meta:
        model = Group
        fields = ("id", "title", "description")

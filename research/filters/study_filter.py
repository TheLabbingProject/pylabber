"""
Definition of the :class:`StudyFilter` class.
"""

from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES
from research.models.study import Study


class StudyFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.study.Study` model.

    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)

    class Meta:
        model = Study
        fields = "id", "title", "description"

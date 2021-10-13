"""
Definition of the :class:`StudyFilter` class.
"""
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from pylabber.utils.configuration import ENABLE_COUNT_FILTERING
from research.filters.utils import LOOKUP_CHOICES
from research.models.procedure import Procedure
from research.models.study import Study

User = get_user_model()


class StudyFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.study.Study` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    n_subjects = filters.RangeFilter(
        label="Number of associated subjects between:"
    )
    collaborators = filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all()
    )
    procedures = filters.ModelMultipleChoiceFilter(
        queryset=Procedure.objects.all()
    )
    if ENABLE_COUNT_FILTERING:
        n_subjects = filters.RangeField(
            label="Number of associated subjects between:"
        )

    class Meta:
        model = Study
        fields = ("id",)

"""
Definition of the :class:`DataAcquisitionFilter` class.
"""
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from research.filters.utils import LOOKUP_CHOICES


class DataAcquisitionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.subject.Subject` model.
    """

    app_label = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    model = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)

    class Meta:
        model = ContentType
        fields = ("id", "app_label", "model")

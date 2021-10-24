"""
Definition of the :class:`TaskResultFilter` class.
"""
from accounts.filters.utils import STATUS_CHOICES
from django_celery_results.models import TaskResult
from django_filters import rest_framework as filters

from pylabber.utils.filters import DEFUALT_LOOKUP_CHOICES


class EmptyCharFilter(filters.CharFilter):
    empty_value = "NULL"

    def filter(self, qs, value):
        if value != self.empty_value:
            return super().filter(qs, value)

        qs = self.get_method(qs)(**{f"{self.field_name}__isnull": True})
        return qs.distinct() if self.distinct else qs


class TaskResultFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~accounts.models.export_destination.ExportDestination` model.
    """

    task_id = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    task_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    worker = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    status = filters.MultipleChoiceFilter(choices=STATUS_CHOICES)
    parent = EmptyCharFilter(lookup_expr="exact", label="Parent task ID:")

    class Meta:
        model = TaskResult
        fields = ("id", "parent")

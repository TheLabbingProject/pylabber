"""
Definition of the :class:`TaskResultFilter` class.
"""
from django_celery_results.models import TaskResult
from django_filters import rest_framework as filters
from utils.lookup_choices import DEFUALT_LOOKUP_CHOICES


class TaskResultFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~accounts.models.export_destination.ExportDestination` model.
    """

    task_id = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    task_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )

    class Meta:
        model = TaskResult
        fields = (
            "id",
            "task_id",
            "task_name",
        )

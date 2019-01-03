from django.db import models
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)


class CharNullField(models.CharField):
    """
    Subclass of the CharField that allows empty strings to be stored as NULL.
    """

    description = "CharField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection):
        """
        Gets value right out of the db and changes it if its ``None``.
        """
        if value is None:
            return ""
        else:
            return value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its ``None``.
        """
        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        if value is None:
            # If db has NULL, convert it to ''.
            return ""

        # Otherwise, just return the value.
        return value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """
        if value == "":
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value


class FilteredTableMixin(SingleTableMixin, FilterView):
    formhelper_class = None
    filterset_class = None
    context_filter_name = "filter"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset().order_by("-id")
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context[self.context_filter_name] = self.filter
        return context

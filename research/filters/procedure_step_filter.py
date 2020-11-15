"""
Definition of the :class:`ProcedureStepFilter` class.
"""

from django_filters import rest_framework as filters
from research.models.procedure_step import ProcedureStep


class ProcedureStepFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.procedure.Procedure` model.

    """

    class Meta:
        model = ProcedureStep
        fields = "id", "index", "procedure"

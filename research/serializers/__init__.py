"""
`Django REST Framework <https://www.django-rest-framework.org/>`_
`serializers <https://www.django-rest-framework.org/api-guide/serializers/>`_
module for the :mod:`research` package.

"""

from research.serializers.group import GroupSerializer
from research.serializers.study import StudySerializer
from research.serializers.subject import SubjectSerializer
from research.serializers.task import TaskSerializer
from research.serializers.event import EventSerializer
from research.serializers.procedure import ProcedureSerializer
from research.serializers.procedure_step import ProcedureStepSerializer
from research.serializers.measurement_definition import (
    MeasurementDefinitionSerializer,
)

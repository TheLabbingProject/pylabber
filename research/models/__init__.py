"""
Definition of the app's models_. For an illustration of the relationship
between the different models, see the :ref:`overview:Overview`.

.. _models:
   https://docs.djangoproject.com/en/3.0/topics/db/models/
"""

from research.models.group import Group
from research.models.study import Study
from research.models.subject import Subject
from research.models.task import Task
from research.models.event import Event
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure

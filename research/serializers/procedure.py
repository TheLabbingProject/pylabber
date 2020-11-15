"""
Definition of the :class:`ProcedureSerializer` class.
"""

from research.models.procedure import Procedure
from rest_framework import serializers


class ProcedureSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.procedure.Procedure` model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    class Meta:
        model = Procedure
        fields = "id", "title", "description"

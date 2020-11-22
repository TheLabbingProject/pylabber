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


class ProcedureItemsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Alternative serializer for the
    :class:`~research.models.procedure.Procedure` model used to generate items
    for select widgets in the frontend.
    """

    value = serializers.IntegerField(source="id")
    text = serializers.CharField(source="title")

    class Meta:
        model = Procedure
        fields = "value", "text"

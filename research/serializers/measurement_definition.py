"""
Definition of the :class:`~research.serializers.measurement_definition.MeasurementDefinitionSerializer` class.
"""

from research.models.measurement_definition import MeasurementDefinition
from rest_framework import serializers


class MeasurementDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.measurement_definition.MeasurementDefinition`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:measurement-detail"
    )

    class Meta:
        model = MeasurementDefinition
        fields = (
            "id",
            "url",
            "title",
            "description",
        )

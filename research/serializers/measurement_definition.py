"""
Definition of the :class:`MeasurementDefinitionSerializer` class.
"""

from research.models.measurement_definition import MeasurementDefinition
from rest_framework import serializers


class MeasurementDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.measurement_definition.MeasurementDefinition`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    app_label = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()

    class Meta:
        model = MeasurementDefinition
        fields = "id", "title", "description", "app_label", "model_name"

    def get_app_label(self, instance: MeasurementDefinition) -> str:
        return instance.content_type.app_label if instance.content_type else ""

    def get_model_name(self, instance: MeasurementDefinition) -> str:
        return instance.content_type.model if instance.content_type else ""

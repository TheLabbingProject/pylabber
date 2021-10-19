"""
Definition of the :class:`MeasurementDefinitionSerializer` class.
"""
from django.contrib.contenttypes.models import ContentType
from research.models.measurement_definition import MeasurementDefinition
from rest_framework import serializers


class MeasurementDefinitionSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for the
    :class:`~research.models.measurement_definition.MeasurementDefinition`
    model.
    """

    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = MeasurementDefinition
        fields = (
            "id",
            "title",
            "description",
            "content_type",
        )

"""
Definition of the :class:`ContentTypeSerializer` class.
"""
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer class for the
    :class:`~django.contrib.contenttypes.models.ContentType`
    model.
    """

    class Meta:
        model = ContentType
        fields = "id", "app_label", "model"

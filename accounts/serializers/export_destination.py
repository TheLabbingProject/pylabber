"""
Definition of the :class:`ExportDestinationSerializer` class.
"""
from accounts.models.export_destination import ExportDestination
from accounts.serializers.user import UserSerializer
from rest_framework import serializers


class ExportDestinationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the
    :class:`~accounts.models.export_destination.ExportDestination` model.
    """

    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ExportDestination
        fields = (
            "id",
            "title",
            "description",
            "ip",
            "username",
            "password",
            "destination",
            "users",
        )

"""
Definition of the :class:`ExportDestinationSerializer` class.
"""
from accounts.models.export_destination import ExportDestination
from accounts.models.user import User
from accounts.serializers.user import UserSerializer
from paramiko import SSHException
from rest_framework import serializers


class ExportDestinationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the
    :class:`~accounts.models.export_destination.ExportDestination` model.
    """

    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        allow_null=True,
        source="users",
        label="User IDs",
        help_text="Sets users access using primary keys.",
        many=True,
        queryset=User.objects.all(),
    )

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
            "user_ids",
            "port",
            "socket_timeout",
            "negotiation_timeout",
            "banner_timeout",
        )

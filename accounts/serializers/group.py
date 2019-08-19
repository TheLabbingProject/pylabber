from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    `Serializer <https://www.django-rest-framework.org/api-guide/serializers/>`_
    class for the :class:`~accounts.models.group.Group` model.
    
    """

    url = serializers.HyperlinkedIdentityField(view_name="accounts:group-detail")

    class Meta:
        model = Group
        fields = ("name",)

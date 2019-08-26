from accounts.models import User
from accounts.models.laboratory import Laboratory
from rest_framework import serializers


class LaboratorySerializer(serializers.HyperlinkedModelSerializer):
    """
    `Serializer <https://www.django-rest-framework.org/api-guide/serializers/>`_
    class for the :class:`~accounts.models.laboratory.Laboratory` model.
    
    """

    url = serializers.HyperlinkedIdentityField(view_name="accounts:laboratory-detail")
    members = serializers.HyperlinkedRelatedField(
        view_name="accounts:user-detail", queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Laboratory
        fields = (
            "id",
            "url",
            "image",
            "title",
            "description",
            "members",
            "created",
            "modified",
        )

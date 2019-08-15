from accounts.models import User
from research.models.laboratory import Laboratory
from rest_framework import serializers


class LaboratorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:laboratory-detail")
    members = serializers.HyperlinkedRelatedField(
        view_name="accounts:user-detail", queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Laboratory
        fields = (
            "id",
            "image",
            "title",
            "description",
            "created",
            "modified",
        )

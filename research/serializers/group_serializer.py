from research.models.group import Group
from research.models.study import Study
from rest_framework import serializers


class MiniStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:study-detail")

    class Meta:
        model = Study
        fields = ("id", "title", "url")


class GroupReadSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:group-detail")
    study = MiniStudySerializer()

    class Meta:
        model = Group
        fields = ("title", "description", "url", "id", "study")


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:group-detail")
    study = serializers.HyperlinkedRelatedField(
        view_name="research:study-detail", queryset=Study.objects.all()
    )

    class Meta:
        model = Group
        fields = ("title", "description", "url", "id", "study")


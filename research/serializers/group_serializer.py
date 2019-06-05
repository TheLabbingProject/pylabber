from research.models.group import Group
from research.models.study import Study
from rest_framework import serializers


class MiniStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ("id", "title")


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:group-detail")
    study = MiniStudySerializer()
    # study = serializers.HyperlinkedRelatedField(
    #     view_name="research:study-detail", queryset=Study.objects.all()
    # )

    class Meta:
        model = Group
        fields = ("title", "description", "url", "id", "study")


from research.models.subject import Subject
from rest_framework import serializers


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:subject-detail")

    class Meta:
        model = Subject
        fields = "__all__"

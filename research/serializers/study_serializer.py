from accounts.models import Profile
from research.models.study import Study
from research.models.subject import Subject
from rest_framework import serializers


class StudySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="research:study-detail")
    subjects = serializers.HyperlinkedRelatedField(
        view_name="research:subject-detail", queryset=Subject.objects.all(), many=True
    )
    collaborators = serializers.HyperlinkedRelatedField(
        view_name="accounts:profile-detail", queryset=Profile.objects.all(), many=True
    )

    class Meta:
        model = Study
        fields = "__all__"

"""
Definition of the :class:`StudySerializer` class.
"""
from accounts.models import User
from pylabber.utils.configuration import ENABLE_COUNT_FILTERING
from research.models.procedure import Procedure
from research.models.study import Study
from research.models.subject import Subject
from rest_framework import serializers


class StudySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the :class:`~research.models.study.Study` model.
    """

    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        allow_null=True,
        many=True,
        required=False,
    )
    collaborators = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        many=True,
        required=False,
    )
    procedures = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all(),
        allow_null=True,
        many=True,
        required=False,
    )
    if ENABLE_COUNT_FILTERING:
        n_subjects = serializers.IntegerField(read_only=True)

    class Meta:
        model = Study
        fields = (
            "id",
            "image",
            "subjects",
            "collaborators",
            "title",
            "description",
            "created",
            "modified",
            "procedures",
            "n_subjects",
        )


class MiniStudySerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer for the :class:`~research.models.study.Study` model.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:study-detail"
    )

    class Meta:
        model = Study
        fields = (
            "id",
            "url",
            "title",
            "description",
        )

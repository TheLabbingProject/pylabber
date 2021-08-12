"""
Definition of the :class:`StudySerializer` class.
"""

from accounts.models import User
from research.models.procedure import Procedure
from research.models.study import Study
from research.models.subject import Subject
from rest_framework import serializers


class StudySerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the :class:`~research.models.study.Study`
    model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:study-detail"
    )
    subjects = serializers.HyperlinkedRelatedField(
        view_name="research:subject-detail",
        queryset=Subject.objects.all(),
        many=True,
    )
    collaborators = serializers.HyperlinkedRelatedField(
        view_name="accounts:user-detail",
        queryset=User.objects.all(),
        many=True,
    )
    procedures = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all(),
        allow_null=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Study
        fields = (
            "id",
            "image",
            "subjects",
            "collaborators",
            "url",
            "title",
            "description",
            "created",
            "modified",
            "procedures",
        )


class MiniStudySerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified HyperlinkedModelSerializer for the
    :class:`~research.models.study.Study` model.
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


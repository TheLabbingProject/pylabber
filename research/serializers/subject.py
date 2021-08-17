"""
Definition of the :class:`SubjectSerializer` class.
"""

from research.models.subject import Subject
from research.serializers.study import MiniStudySerializer
from rest_framework import serializers


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.subject.Subject` model.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="research:subject-detail"
    )
    latest_mri_session_time = serializers.DateTimeField(read_only=True)
    mri_session_count = serializers.SerializerMethodField(read_only=True)
    studies = MiniStudySerializer(source="query_studies", many=True)

    class Meta:
        model = Subject
        fields = (
            "id",
            "url",
            "id_number",
            "first_name",
            "last_name",
            "date_of_birth",
            "dominant_hand",
            "sex",
            "gender",
            "custom_attributes",
            "mri_session_count",
            "latest_mri_session_time",
            "created",
            "modified",
            "studies",
        )

    def get_mri_session_count(self, subject: Subject) -> int:
        return subject.mri_session_set.count()

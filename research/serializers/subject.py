"""
Definition of the :class:`SubjectSerializer` class.
"""
from typing import Tuple

from research.models.subject import Subject
from research.serializers.study import MiniStudySerializer
from rest_framework import serializers

NON_PERSONAL_INFORMATION_FIELDS: Tuple[str] = (
    "id",
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
PERSONAL_INFORMATION_FIELDS: Tuple[str] = (
    "id_number",
    "first_name",
    "last_name",
)


class SubjectSerializer(serializers.ModelSerializer):
    """
    Base serializer for the :class:`~research.models.subject.Subject` model.
    """

    latest_mri_session_time = serializers.DateTimeField(read_only=True)
    mri_session_count = serializers.IntegerField(read_only=True)
    studies = MiniStudySerializer(source="query_studies", many=True)

    class Meta:
        model = Subject
        fields = NON_PERSONAL_INFORMATION_FIELDS


class AdminSubjectSerializer(SubjectSerializer):
    class Meta:
        model = Subject
        fields = tuple(
            list(PERSONAL_INFORMATION_FIELDS)
            + list(NON_PERSONAL_INFORMATION_FIELDS)
        )

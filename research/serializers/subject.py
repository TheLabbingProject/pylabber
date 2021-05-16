"""
Definition of the :class:`SubjectSerializer` class.
"""

from research.models.subject import Subject
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
    latest_mri_session_time = serializers.SerializerMethodField()
    mri_session_count = serializers.SerializerMethodField()

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
        )

    def get_latest_mri_session_time(self, instance: Subject):
        sessions = instance.mri_session_set.order_by("-time")
        return sessions.first().time if sessions.exists() else None

    def get_mri_session_count(self, instance: Subject):
        return instance.mri_session_set.count()

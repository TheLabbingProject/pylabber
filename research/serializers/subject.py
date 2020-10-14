"""
Definition of the :class:`~research.serializers.subject.SubjectSerializer` class.
"""

from research.models.subject import Subject
from django_mri.serializers import SessionSerializer
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
    mri_session_set = SessionSerializer(many=True, required=False)

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
            "mri_session_set",
        )

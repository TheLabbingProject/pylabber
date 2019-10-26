from research.models.subject import Subject
from rest_framework import serializers


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    `HyperlinkedModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer>`_
    for the :class:`~research.models.subject.Subject` model.

    """

    url = serializers.HyperlinkedIdentityField(view_name="research:subject-detail")

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
        )

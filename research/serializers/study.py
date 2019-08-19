from accounts.models import User
from research.models.study import Study
from research.models.subject import Subject
from rest_framework import serializers


class StudySerializer(serializers.HyperlinkedModelSerializer):
    """
    `HyperlinkedModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer>`_
    for the :class:`~research.models.study.Study` model.
    
    """

    url = serializers.HyperlinkedIdentityField(view_name="research:study-detail")
    subjects = serializers.HyperlinkedRelatedField(
        view_name="research:subject-detail", queryset=Subject.objects.all(), many=True
    )
    collaborators = serializers.HyperlinkedRelatedField(
        view_name="accounts:user-detail", queryset=User.objects.all(), many=True
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
        )

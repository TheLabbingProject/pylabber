from research.models.group import Group
from research.models.study import Study
from rest_framework import serializers


class MiniStudySerializer(serializers.ModelSerializer):
    """
    A minimized :class:`~research.models.study.Study`
    `ModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#modelserializer>`_
    used in the :class:`~research.serializers.group.GroupReadSerializer` class.
    
    """

    url = serializers.HyperlinkedIdentityField(view_name="research:study-detail")

    class Meta:
        model = Study
        fields = ("id", "title", "url")


class GroupReadSerializer(serializers.HyperlinkedModelSerializer):
    """
    `HyperlinkedModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer>`_
    for the :class:`~research.models.group.Group` model to be used in GET requests.

    """

    url = serializers.HyperlinkedIdentityField(view_name="research:group-detail")
    study = MiniStudySerializer()

    class Meta:
        model = Group
        fields = ("title", "description", "url", "id", "study")


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    `HyperlinkedModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer>`_
    for the :class:`~research.models.group.Group` model to be used in POST requests.

    """

    url = serializers.HyperlinkedIdentityField(view_name="research:group-detail")
    study = serializers.HyperlinkedRelatedField(
        view_name="research:study-detail", queryset=Study.objects.all()
    )

    class Meta:
        model = Group
        fields = ("title", "description", "url", "id", "study")


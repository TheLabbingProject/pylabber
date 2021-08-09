"""
Definition of the :class:`GroupSerializer` class.
"""
from research.models.group import Group
from research.models.study import Study
from rest_framework import serializers


class MiniStudySerializer(serializers.ModelSerializer):
    """
    A minimized :class:`~research.models.study.Study`
    ModelSerializer_ used in the
    :class:`~research.serializers.group.GroupReadSerializer` class.

    .. _ModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
    """

    class Meta:
        model = Study
        fields = "id", "title"


class GroupReadSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.group.Group` model to be used in GET requests.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    study = MiniStudySerializer()

    class Meta:
        model = Group
        fields = "id", "title", "description", "study"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer_ for the
    :class:`~research.models.group.Group` model to be used in POST requests.

    .. _HyperlinkedModelSerializer:
       https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    """

    study = serializers.PrimaryKeyRelatedField(queryset=Study.objects.all())

    class Meta:
        model = Group
        fields = "id", "title", "description", "study"

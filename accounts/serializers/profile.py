from accounts.models import Profile

# from accounts.serializers.user import UserSerializer
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    `Serializer <https://www.django-rest-framework.org/api-guide/serializers/>`_
    class for the :class:`~accounts.models.profile.Profile` model.
    """

    url = serializers.HyperlinkedIdentityField(view_name="accounts:profile-detail")

    class Meta:
        model = Profile
        fields = (
            "title",
            "image",
            "date_of_birth",
            "institute",
            "bio",
            "url",
        )

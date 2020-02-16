from accounts.models.profile import Profile
from accounts.models.user import User
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from accounts.serializers.profile import ProfileSerializer


class UserSerializer(UserDetailsSerializer):
    """
    `Serializer <https://www.django-rest-framework.org/api-guide/serializers/>`_
    class for the :class:`~accounts.models.user.User` model.
    """

    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")
    profile = ProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "url",
            "id",
            "profile",
            "is_staff",
            "laboratory_set",
        )

    def update(self, username, data):
        profile_data = data.pop("profile", {})
        super().update(username, data)
        if profile_data:
            profile = Profile.objects.filter(user__username=username)
            profile.update(**profile_data)
        updated_user = User.objects.get(username=username)
        return updated_user

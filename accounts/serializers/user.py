"""
Definition of the :class:`~accounts.serializers.user.UserSerializer` class.
"""
from accounts.models.profile import Profile
from accounts.models.user import User
from accounts.serializers.profile import ProfileSerializer
from dj_rest_auth.serializers import UserDetailsSerializer


class UserSerializer(UserDetailsSerializer):
    """
    Serializer class for the :class:`~accounts.models.user.User` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    profile = ProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "profile",
            "is_staff",
            "is_superuser",
            "laboratory_set",
        )

    def update(self, username, data: dict):
        """
        Update a user's personal information, including profile data.

        Parameters
        ----------
        username : ~accounts.models.user.User
            User to be updated
        data : dict
            User information

        Returns
        -------
        ~accounts.models.user.User
            Updated user instance
        """

        profile_data = data.pop("profile", {})
        super().update(username, data)
        if profile_data:
            profile = Profile.objects.filter(user__username=username)
            profile.update(**profile_data)
        updated_user = User.objects.get(username=username)
        return updated_user

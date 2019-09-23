from accounts.models.profile import Profile
from accounts.models.user import User
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer


class UserSerializer(UserDetailsSerializer):
    """
    `Serializer <https://www.django-rest-framework.org/api-guide/serializers/>`_
    class for the :class:`~accounts.models.user.User` model.
    
    """

    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")
    image = serializers.ImageField(source="profile.image")
    title = serializers.CharField(source="profile.title")
    date_of_birth = serializers.DateField(source="profile.date_of_birth")
    institute = serializers.CharField(source="profile.institute")
    bio = serializers.CharField(source="profile.bio", allow_blank=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "url",
            "id",
            "image",
            "title",
            "date_of_birth",
            "institute",
            "bio",
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

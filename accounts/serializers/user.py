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
    position = serializers.CharField(source="profile.position")
    date_of_birth = serializers.DateField(source="profile.date_of_birth")
    institute = serializers.CharField(source="profile.institute")
    bio = serializers.CharField(source="profile.bio")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "url",
            "id",
            "image",
            "title",
            "position",
            "date_of_birth",
            "institute",
            "bio",
            "is_staff",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance = super().update(instance, validated_data)
        if profile_data:
            instance.profile.update(profile_data)
        return instance

from accounts.models import Profile, User
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:group-detail")

    class Meta:
        model = Group
        fields = ("url", "name")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ("id", "url", "username", "email", "first_name", "last_name")


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:profile-detail")
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"

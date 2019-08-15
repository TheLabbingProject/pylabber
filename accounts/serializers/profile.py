from accounts.models import Profile
from accounts.serializers.user import UserSerializer
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:profile-detail")
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"

from accounts.models.profile import Profile
from accounts.serializers.profile import ProfileSerializer
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class ProfileViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.profile.Profile` instances to
    be viewed or edited.
    
    """

    queryset = Profile.objects.all().order_by("-user__date_joined")
    serializer_class = ProfileSerializer

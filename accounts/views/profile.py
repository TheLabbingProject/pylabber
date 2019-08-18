from accounts.models.profile import Profile
from accounts.serializers.profile import ProfileSerializer
from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class ProfileViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows user profles to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Profile.objects.all().order_by("-user__date_joined")
    serializer_class = ProfileSerializer

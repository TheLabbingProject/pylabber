from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model
from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows user profles to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = get_user_model().objects.all().order_by("date_joined")
    serializer_class = UserSerializer

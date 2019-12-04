from accounts.filters.user import UserFilter
from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.user.User` instances to
    be viewed or edited.

    """

    filter_class = UserFilter
    queryset = get_user_model().objects.all().order_by("date_joined")
    serializer_class = UserSerializer

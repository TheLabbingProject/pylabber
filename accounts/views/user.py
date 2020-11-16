"""
Definition of the :class:`~accounts.views.user.UserViewSet` class.
"""

from accounts.filters.user import UserFilter
from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.user.User` instances to
    be viewed or edited.

    """

    filter_class = UserFilter
    queryset = get_user_model().objects.all().order_by("date_joined")
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def get_institutions(self, request):
        queryset = self.get_queryset()
        institutions = set(
            value
            for value in queryset.values_list("profile__institute", flat=True)
            if value is not None
        )
        data = {"results": institutions}
        return Response(data)

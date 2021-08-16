"""
Definition of the :class:`UserViewSet` class.
"""
from accounts.filters.user import UserFilter
from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.user.User` instances to
    be viewed or edited.
    """

    filter_class = UserFilter
    queryset = User.objects.all().order_by("date_joined")
    serializer_class = UserSerializer

    def filter_queryset(self, queryset) -> QuerySet:
        """
        Filter the returned users according to the requesting user's
        permissions.

        Parameters
        ----------
        queryset : QuerySet
            Base queryset

        Returns
        -------
        QuerySet
            User instances
        """
        user = self.request.user
        queryset = super().filter_queryset(queryset)
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(laboratory__in=user.laboratory_set.all())

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

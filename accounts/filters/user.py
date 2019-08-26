from accounts.models.user import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    """
    Provides useful filtering options for the :class:`~accounts.models.user.User`
    model.
    
    """

    class Meta:
        model = User
        fields = ("id", "username")


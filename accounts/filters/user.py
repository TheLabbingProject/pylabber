"""
Definition of the :class:`UserFilter` class.
"""
from accounts.models.user import User
from django_filters import rest_framework as filters
from pylabber.utils.filters import DEFUALT_LOOKUP_CHOICES


class UserFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~accounts.models.user.User` model.
    """

    username = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    first_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    last_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    email = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
    institute = filters.AllValuesMultipleFilter(
        field_name="profile__institute"
    )
    study_ne = filters.NumberFilter(field_name="study", exclude=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "institute",
            "study",
            "study_ne",
        )

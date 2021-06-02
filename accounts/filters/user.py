"""
Definition of the :class:`UserFilter` class.
"""
from accounts.models.user import User
from django_filters import rest_framework as filters


LOOKUP_CHOICES = [
    ("contains", "Contains (case-sensitive)"),
    ("icontains", "Contains (case-insensitive)"),
    ("exact", "Exact"),
]


class UserFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~accounts.models.user.User` model.
    """

    username = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    first_name = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    last_name = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    email = filters.LookupChoiceFilter(lookup_choices=LOOKUP_CHOICES)
    institute = filters.AllValuesFilter(field_name="profile__institute")
    study = filters.NumberFilter(field_name="study", lookup_expr="exact")
    study_ne = filters.NumberFilter(
        field_name="study", lookup_expr="exact", exclude=True
    )

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

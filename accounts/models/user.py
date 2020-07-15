"""
Definition of the :class:`~accounts.models.user.User` model.
"""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model definition.

    References
    ----------
    * `Using a custom user model when starting a project`_.

    .. _Using a custom user model when starting a project:
       https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

    """

    pass

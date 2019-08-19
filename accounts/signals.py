from accounts.models import Profile
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    """
    Standard implementation for user profile creation.

    Parameters
    ----------
    sender : django.db.models.Model
        The class of the instance being saved
    instance : django.db.models.Model
        The instance being saved
    created : bool
        Whether the instance is being created or updated

    """

    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            print("failed to create user profile with the following exception:")
            print(e)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Automatically creates an authentication token for the user, as described in
    `the DRF documentation <https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens>`_.
    
    Parameters
    ----------
    created : bool, optional
        Whether the instance is being created or updated, by default False
    """

    if created:
        Token.objects.create(user=instance)

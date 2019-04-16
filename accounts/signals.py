from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import Profile


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

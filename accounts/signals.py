from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from . import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            models.Profile.objects.create(user=instance)
        except Exception as e:
            print(
                'failed to create user profile with the following exception:')
            print(e)

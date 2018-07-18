from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    def get_short_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name[0]}. {self.last_name}'
        else:
            return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.user.id)])

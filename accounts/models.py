from accounts.choices import Title
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    image = models.ImageField(
        upload_to='images',
        blank=True,
    )
    title = models.CharField(
        max_length=20,
        choices=Title.choices(),
        default=Title.NONE,
    )
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.user.id)])

    def get_full_name(self):
        full_name = f'{self.user.first_name} {self.user.last_name}'
        if self.title:
            return full_name + f', {Title[self.title].value}.'
        return full_name

    def get_study_list(self):
        return [study.name for study in self.user.studies.all()]

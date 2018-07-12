from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Study(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collaborators = models.ManyToManyField(get_user_model())

    class Meta:
        verbose_name_plural = 'Studies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('study_detail', args=[str(self.id)])

from django.db import models
from django.forms import PasswordInput
from django.urls import reverse
from .choices import DataSourceType


class DataSource(models.Model):
    name = models.CharField(max_length=64, blank=True)
    source_type = models.CharField(
        max_length=3,
        choices=DataSourceType.choices(),
        blank=True,
    )

    class Meta:
        abstract = True


class SMBDirectory(DataSource):
    user_id = models.CharField(max_length=64, blank=False)
    password = models.CharField(max_length=64, blank=False)
    share_name = models.CharField(max_length=64, blank=False)
    client_name = models.CharField(max_length=64, blank=False)
    server_name = models.CharField(max_length=64, blank=False)
    server_ip = models.GenericIPAddressField(blank=False)

    def get_absolute_url(self):
        return reverse('data_source_detail', args=[str(self.id)])

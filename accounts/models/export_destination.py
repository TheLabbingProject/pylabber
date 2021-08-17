from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from mirage import fields


class ExportDestination(TitleDescriptionModel):
    ip = models.GenericIPAddressField(
        blank=False, null=False, verbose_name="IP"
    )
    username = models.CharField(max_length=128, blank=False, null=False)
    password = fields.EncryptedCharField(
        max_length=128, blank=False, null=False
    )
    destination = models.CharField(max_length=512, blank=False, null=False)
    users = models.ManyToManyField("accounts.User")

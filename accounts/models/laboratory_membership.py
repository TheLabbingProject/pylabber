from accounts.models.choices import Role
from django.db import models


class LaboratoryMembership(models.Model):
    laboratory = models.ForeignKey("accounts.Laboratory", on_delete=models.CASCADE)
    member = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20, choices=Role.choices(), default="", blank=True, null=True
    )


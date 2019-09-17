from accounts.models.choices import Position
from django.db import models


class LabMembership(models.Model):
    lab = models.ForeignKey("accounts.Laboratory", on_delete=models.CASCADE)
    member = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    # The role of the reseacher in the lab
    position = models.CharField(
        max_length=20, choices=Position.choices(), default="", blank=True, null=True
    )

    class Meta:
        verbose_name = "Laboratory Membership"


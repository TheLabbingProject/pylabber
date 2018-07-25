from django.db import models
from .choices import Sex
from .validators import digits_only


class Patient(models.Model):
    patient_uid = models.CharField(
        max_length=64,
        unique=True,
        validators=[digits_only],
    )
    given_name = models.CharField(max_length=64, blank=True)
    family_name = models.CharField(max_length=64, blank=True)
    middle_name = models.CharField(max_length=64, blank=True)
    name_prefix = models.CharField(max_length=64, blank=True)
    name_suffix = models.CharField(max_length=64, blank=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    sex = models.CharField(
        max_length=1,
        choices=Sex.choices(),
        blank=True,
    )

    subject = models.OneToOneField(
        'research.Subject',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.patient_uid

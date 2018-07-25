from django.db import models
from django.urls import reverse
from .choices import Sex, Gender, DominantHand
from .validators import digits_only


class Subject(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    date_of_birth = models.DateField(
        verbose_name='Date of Birth',
        blank=True,
        null=True,
    )

    id_number = models.CharField(
        max_length=9,
        validators=[digits_only],
        blank=True,
    )
    phone_number = models.CharField(
        max_length=50,
        validators=[digits_only],
        blank=True,
    )

    dominant_hand = models.CharField(
        max_length=5,
        choices=DominantHand.choices(),
        default=DominantHand.RIGHT,
        blank=True,
    )

    sex = models.CharField(
        max_length=6,
        choices=Sex.choices(),
        blank=True,
    )

    gender = models.CharField(
        max_length=5,
        choices=Gender.choices(),
        default=Gender.CIS,
        blank=True,
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return self.last_name[:2] + self.first_name[:2]
        elif self.id_number:
            return self.id_number
        return f'Subject #{self.id}'

    def get_absolute_url(self):
        return reverse('subject_detail', args=[str(self.id)])

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

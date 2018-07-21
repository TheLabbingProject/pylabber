from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


class Subject(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name='Date of Birth')

    digits_only = RegexValidator(
        '^\d+$',
        message='Digits only!',
        code='invalid_number',
    )
    id_number = models.CharField(
        max_length=9,
        blank=True,
        validators=[digits_only],
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        validators=[digits_only],
    )

    RIGHT = 'R'
    LEFT = 'L'
    AMBIDEXTROUS = 'A'
    DOMINANT_HAND_CHOICES = [
        (RIGHT, 'Right'),
        (LEFT, 'Left'),
        (AMBIDEXTROUS, 'Ambidextrous'),
    ]
    dominant_hand = models.CharField(
        max_length=1,
        choices=DOMINANT_HAND_CHOICES,
        default=RIGHT,
    )

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
    )

    CISGENDER = 'C'
    TRANSGENDER = 'T'
    GENDER_CHOICES = [
        (CISGENDER, 'Cisgender'),
        (TRANSGENDER, 'Transgender'),
        (OTHER, 'Other'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=CISGENDER,
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


class Study(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    subjects = models.ManyToManyField(Subject, related_name='studies')
    collaborators = models.ManyToManyField(
        get_user_model(), related_name='studies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Studies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('study_detail', args=[str(self.id)])

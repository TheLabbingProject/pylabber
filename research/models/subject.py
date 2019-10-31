from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from pylabber.utils import CharNullField
from research.utils.custom_attributes_processor import CustomAttributesProcessor
from .choices import Sex, Gender, DominantHand
from .validators import digits_only, not_future


class Subject(TimeStampedModel):
    """
    A model to represent a single research subject. Any associated data model
    should have this model's primary key as a relation.

    """

    id_number = CharNullField(
        max_length=64, unique=True, validators=[digits_only], blank=True, null=True
    )
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", blank=True, null=True, validators=[not_future]
    )
    dominant_hand = models.CharField(
        max_length=5, choices=DominantHand.choices(), blank=True, null=True
    )
    sex = models.CharField(max_length=6, choices=Sex.choices(), blank=True, null=True)
    gender = models.CharField(
        max_length=5, choices=Gender.choices(), blank=True, null=True
    )
    custom_attributes = JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Subject #{self.id}"

    def get_absolute_url(self):
        return reverse("research:subject_detail", args=[str(self.id)])

    def get_full_name(self) -> str:
        """
        Returns a formatted string with the subject's full name (first name
        and then last name).

        Returns
        -------
        str
            Subject's full name
        """

        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        custom_attributes_processor = CustomAttributesProcessor(self.custom_attributes)
        custom_attributes_processor.validate()
        super().save(*args, **kwargs)


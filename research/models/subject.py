from django.db import models
from django.urls import reverse
from pylabber.utils import CharNullField
from .choices import Sex, Gender, DominantHand
from .validators import digits_only, not_future


class Subject(models.Model):
    id_number = CharNullField(
        max_length=64, unique=True, validators=[digits_only], blank=True, null=True
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", blank=True, null=True, validators=[not_future]
    )
    dominant_hand = models.CharField(
        max_length=5, choices=DominantHand.choices(), blank=True
    )
    sex = models.CharField(max_length=6, choices=Sex.choices(), blank=True)
    gender = models.CharField(max_length=5, choices=Gender.choices(), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_number

    def get_absolute_url(self):
        return reverse("research:subject_detail", args=[str(self.id)])

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_tree(self):
        return {
            "id": str(self.id),
            "text": self.get_full_name(),
            "icon": "fas fa-user",
            "children": [
                {
                    "id": f"{self.id}_mri",
                    "icon": "fab fa-magento",
                    "text": "MRI",
                    "children": self.get_dicom_patient().to_tree(),
                }
            ],
        }


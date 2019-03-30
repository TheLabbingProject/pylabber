from django.db import models
from mri.models.choices import ScanningSequence, SequenceVariant
from mri.models.fields import ChoiceArrayField


class SequenceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)

    scanning_sequence = ChoiceArrayField(
        models.CharField(max_length=2, choices=ScanningSequence.choices()),
        size=5,
        blank=True,
        null=True,
    )
    sequence_variant = ChoiceArrayField(
        models.CharField(max_length=4, choices=SequenceVariant.choices()),
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ("scanning_sequence", "sequence_variant")

    def __str__(self):
        return self.name

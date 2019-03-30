from django.db import models
from mri.models.sequence_type import SequenceType


class ScanManager(models.Manager):
    def get_anatomicals(self):
        mprage = SequenceType.objects.get(name="MPRAGE")
        return self.filter(sequence_type=mprage).order_by(
            "-time__date", "spatial_resolution"
        )

    def get_default_anatomical(self):
        return self.get_anatomicals().first()

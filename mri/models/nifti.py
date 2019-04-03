import nibabel as nib
import numpy as np
import os

from django.db import models
from django_extensions.db.models import TimeStampedModel
from mri.models.managers import NIfTIManager
from research.models import Subject


class NIfTI(TimeStampedModel):
    path = models.FilePathField(max_length=500, unique=True)
    is_raw = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "mri.Scan",
        on_delete=models.CASCADE,
        related_name="derived_niftis",
        blank=True,
        null=True,
    )

    objects = NIfTIManager()

    def get_data(self) -> np.ndarray:
        return nib.load(self.path).get_data()

    @property
    def b_value(self) -> list:
        file_name = self.path.replace("nii.gz", "bval")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            content = content.splitlines()[0].split("\t")
            return [int(value) for value in content]
        return None

    @property
    def b_vector(self) -> list:
        file_name = self.path.replace("nii.gz", "bvec")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            return [
                [float(value) for value in vector.rstrip().split("\t")]
                for vector in content.rstrip().split("\n")
            ]
        return None

    @property
    def subject(self) -> Subject:
        try:
            return self.parent.subject
        except AttributeError:
            return None

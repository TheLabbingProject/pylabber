import nibabel as nib
import numpy as np
import os
import sklearn.metrics

from django.db import models


class NIfTI(models.Model):
    path = models.FilePathField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_data(self) -> np.ndarray:
        return nib.load(self.path).get_data()

    def calculate_mutual_information(self, other, bins: int = 10) -> np.float64:
        self_data = self.get_data().flatten()
        other_data = other.get_data().flatten()
        histogram = np.histogram2d(self_data, other_data, bins)[0]
        return sklearn.metrics.mutual_info_score(None, None, contingency=histogram)

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

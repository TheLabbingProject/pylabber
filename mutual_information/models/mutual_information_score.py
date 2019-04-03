import numpy as np
import sklearn.metrics

from django.db import models
from mutual_information.models.managers import MutualInformationScoreManager


class MutualInformationScore(models.Model):
    histogram_bins = models.IntegerField()
    value = models.FloatField()
    is_self_score = models.BooleanField(default=False)

    one_scan = models.ForeignKey(
        "mri.Scan", on_delete=models.CASCADE, related_name="_mutual_information_scores"
    )
    second_scan = models.ForeignKey(
        "mri.Scan", on_delete=models.CASCADE, related_name="mutual_information_scores"
    )
    one_nifti = models.ForeignKey(
        "mri.NIfTI", on_delete=models.CASCADE, related_name="mi_scores", null=True
    )
    second_nifti = models.ForeignKey(
        "mri.NIfTI", on_delete=models.CASCADE, related_name="mi_scoress", null=True
    )

    objects = MutualInformationScoreManager()

    def get_histogram(self) -> np.ndarray:
        one = self.one_scan.brain_in_mni.get_data().flatten()
        two = self.second_scan.brain_in_mni.get_data().flatten()
        return np.histogram2d(one, two, self.histogram_bins)[0]

    def calculate(self) -> np.float64:
        histogram = self.get_histogram()
        return sklearn.metrics.mutual_info_score(None, None, contingency=histogram)

    def check_if_self_score(self) -> bool:
        return self.one_scan.subject == self.second_scan.subject


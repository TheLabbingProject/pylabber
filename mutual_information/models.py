from django.db import models


class MutualInformationScoreManager(models.Manager):
    def get(self, first_scan, second_scan, histogram_bins):
        try:
            return self.get(
                first_scan=first_scan,
                second_scan=second_scan,
                histogram_bins=histogram_bins,
            )
        except models.ObjectDoesNotExist:
            return self.get(
                first_scan=second_scan,
                second_scan=first_scan,
                histogram_bins=histogram_bins,
            )


class MutualInformationScore(models.Model):
    histogram_bins = models.IntegerField()
    value = models.FloatField()

    first_scan = models.ForeignKey("mri.Scan", on_delete=models.CASCADE)
    second_scan = models.ForeignKey("mri.Scan", on_delete=models.CASCADE)


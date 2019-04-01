import numpy as np
import pandas as pd
import sklearn.metrics

from django.db import models, IntegrityError
from mri.models import Scan
from research.models import Subject


class MutualInformationScoreManager(models.Manager):
    def filter_by_scans(self, one_scan: Scan, second_scan: Scan) -> models.QuerySet:
        return self.filter(
            models.Q(one_scan=one_scan, second_scan=second_scan)
            | models.Q(one_scan=second_scan, second_scan=one_scan)
        )

    def filter_by_scan(self, scan: Scan):
        return self.filter(models.Q(one_scan=scan) | models.Q(second_scan=scan))

    def get_score(self, one_scan: Scan, second_scan: Scan, bins: int) -> float:
        query = self.filter_by_scans(one_scan, second_scan).filter(histogram_bins=bins)
        if query.count() == 1:
            return query.first().value
        elif query.count() == 0:
            return None
        else:
            raise IntegrityError("Multiple scores found for the given arguments!")

    def create_and_calculate(
        self, one_scan: Scan, second_scan: Scan, histogram_bins: int
    ):
        instance = self.model(
            one_scan=one_scan, second_scan=second_scan, histogram_bins=histogram_bins
        )
        instance.value = instance.calculate()
        instance.save()
        return instance

    def create_subject_scores(
        self, subject: Subject, histogram_bins: int
    ) -> models.QuerySet:
        anatomical = subject.scan_set.get_default_anatomical()
        for other in Subject.objects.exclude(id=subject.id).all():
            other_anatomical = other.scan_set.get_default_anatomical()
            if other_anatomical:
                existing_score = MutualInformationScore.objects.get_score(
                    anatomical, other_anatomical, histogram_bins
                )
                if not existing_score:
                    self.create_and_calculate(
                        one_scan=anatomical,
                        second_scan=other_anatomical,
                        histogram_bins=histogram_bins,
                    )
        return self.filter_by_scan(anatomical).filter(histogram_bins=histogram_bins)

    def generate_scan_df(self, scan: Scan) -> pd.DataFrame:
        records = list(self.filter_by_scan(scan).values())
        df = pd.DataFrame.from_records(records)
        df.set_index("id", inplace=True)
        df["subject_id"] = None
        for index, row in df.iterrows():
            scan_one = Scan.objects.get(id=row["one_scan_id"])
            scan_two = Scan.objects.get(id=row["second_scan_id"])
            if scan_one == scan:
                other_subject = scan_two.subject.id_number
            else:
                other_subject = scan_one.subject.id_number
            df.loc[index, "subject_id"] = other_subject
        return df

    def generate_df(self) -> pd.DataFrame:
        records = list(self.values())
        df = pd.DataFrame.from_records(records)
        df["is_self"] = df.apply(
            lambda score: self.get(id=score["id"]).one_scan.subject
            == self.get(id=score["id"]).second_scan.subject,
            axis=1,
        )
        return df


class MutualInformationScore(models.Model):
    histogram_bins = models.IntegerField()
    value = models.FloatField()

    one_scan = models.ForeignKey(
        "mri.Scan", on_delete=models.CASCADE, related_name="_mutual_information_scores"
    )
    second_scan = models.ForeignKey(
        "mri.Scan", on_delete=models.CASCADE, related_name="mutual_information_scores"
    )

    objects = MutualInformationScoreManager()

    def calculate(self) -> np.float64:
        one = self.one_scan.brain_in_mni.get_data().flatten()
        two = self.second_scan.brain_in_mni.get_data().flatten()
        histogram = np.histogram2d(one, two, self.histogram_bins)[0]
        return sklearn.metrics.mutual_info_score(None, None, contingency=histogram)

import numpy as np

from django.db import models
from .patient import Patient
from .study import Study
from .validators import digits_and_dots_only


class Series(models.Model):
    series_uid = models.CharField(
        max_length=64,
        unique=True,
        validators=[digits_and_dots_only],
    )
    number = models.IntegerField(verbose_name='Series Number')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=64)
    study = models.ForeignKey(
        Study, blank=True, null=True, on_delete=models.PROTECT)
    patient = models.ForeignKey(
        Patient, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.series_uid

    def get_data(self) -> np.ndarray:
        instances = self.instance_set.order_by('number')
        return np.stack(
            [instance.read_data().pixel_array for instance in instances],
            axis=-1)

    class Meta:
        verbose_name_plural = 'Series'

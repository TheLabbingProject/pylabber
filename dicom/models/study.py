from django.db import models
from django.urls import reverse
from .validators import digits_and_dots_only


class Study(models.Model):
    study_uid = models.CharField(
        max_length=64,
        unique=True,
        validators=[digits_and_dots_only],
    )
    description = models.CharField(max_length=64)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.study_uid

    def get_absolute_url(self):
        return reverse('dicom_study_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'Studies'

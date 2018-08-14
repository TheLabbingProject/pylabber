import numpy as np

from django.db import models
from .question import Question


class RatingQuestion(Question):
    min_value = models.FloatField(default=0)
    min_label = models.CharField(max_length=64, blank=True, default='')
    max_value = models.FloatField(default=4)
    max_label = models.CharField(max_length=64, blank=True, default='')
    steps = models.IntegerField(default=5)

    def get_range(self):
        return np.linspace(self.min_value, self.max_value, self.steps)
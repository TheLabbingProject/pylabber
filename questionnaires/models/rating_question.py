from django.db import models
from .question import Question


class RatingQuestion(Question):
    min_value = models.FloatField(default=0)
    max_value = models.FloatField(default=4)
    steps = models.IntegerField(default=5)
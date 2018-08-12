from django.db import models
from .answer import Answer


class RatingAnswer(Answer):
    value = models.FloatField()

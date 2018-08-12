from django.db import models
from .answer import Answer


class ShortOpenAnswer(Answer):
    text = models.CharField(max_length=255)


class LongOpenAnswer(Answer):
    text = models.TextField(max_length=1000)

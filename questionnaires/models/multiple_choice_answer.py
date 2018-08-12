from django.db import models
from .answer import Answer
from .option import Option


class MultipleChoiceAnswer(Answer):
    choice = models.ForeignKey(Option, on_delete=models.PROTECT)

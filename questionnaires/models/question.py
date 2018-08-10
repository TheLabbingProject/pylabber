from django.db import models
from .option import Option
from .questionnaire import Questionnaire


class Question(models.Model):
    text = models.TextField(max_length=1000)

    options = models.ManyToManyField(
        Option,
        related_name='option_for',
    )
    solution = models.ForeignKey(
        Option,
        related_name='solution_for',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    questionnaires = models.ManyToManyField(
        Questionnaire,
        related_name='questions',
    )

    def __str__(self):
        return self.text

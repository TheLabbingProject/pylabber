from django.db import models
from .option import Option
from .question import Question


class MultipleChoiceQuestion(Question):
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

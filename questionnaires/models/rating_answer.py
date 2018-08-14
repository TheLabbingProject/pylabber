from django.db import models
from .answer import Answer


class RatingAnswer(Answer):
    value = models.FloatField()

    def validate_range(self) -> None:
        min_value = self.question.ratingquestion.min_value
        max_value = self.question.ratingquestion.max_value
        if not min_value < self.value < max_value:
            raise ValueError(
                f'Invalid value! Must be between {min_value} and {max_value}.')

    def save(self, *args, **kwargs):
        self.validate_range()
        super(RatingAnswer, self).save(*args, **kwargs)

from django.db import models
from django.urls import reverse
from .question import Question
from .rating_question import RatingQuestion


class Questionnaire(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    questions = models.ManyToManyField(
        Question,
        related_name='questionnaires',
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('questionnaire_detail', args=[str(self.id)])

    def get_rating_questions(self):
        return [
            question for question in self.questions.all()
            if hasattr(question, 'ratingquestion')
        ]

    def get_open_questions(self):
        return [
            question for question in self.questions.all()
            if hasattr(question, 'openquestion')
        ]

    def get_multiple_choice_questions(self):
        return [
            question for question in self.questions.all()
            if hasattr(question, 'multiplechoicequestion')
        ]
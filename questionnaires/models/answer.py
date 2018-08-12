# import pandas as pd

# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
from django.db import models
from .question import Question
from .questionnaire import Questionnaire


class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    subject = models.ForeignKey('research.Subject', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.subject} answer to {self.question}'


# class AnswerManager(models.Manager):
#     def from_xlsx(self, file):
#         dest_name = default_storage.save('tmp.xlsx', ContentFile(file.read()))
#         df = pd.read_excel(dest_name)

# class Answer(models.Model):
#     questionnaire = models.ForeignKey(Questionnaire, on_delete=models.PROTECT)
#     question = models.ForeignKey(Question, on_delete=models.PROTECT)
#     choice = models.ForeignKey(Option, on_delete=models.PROTECT)
#     subject = models.ForeignKey('research.Subject', on_delete=models.PROTECT)

#     def __str__(self):
#         return str(self.choice)

#     # This is written this way instead of as a simple property in favor of
#     # preserving the nice V and X icons in the Django admin.
#     def _is_correct(self) -> bool:
#         if self.question.solution:
#             return self.choice == self.question.solution
#         return

#     _is_correct.boolean = True
#     is_correct = property(_is_correct)

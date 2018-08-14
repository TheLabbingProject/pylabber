from django.db import models


class Question(models.Model):
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.text

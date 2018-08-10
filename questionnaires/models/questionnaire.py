from django.db import models

# from django.urls import reverse


class Questionnaire(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('questionnaire_detail', args=[str(self.id)])

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from .subject import Subject


class Study(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(
        upload_to='images/studies',
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    subjects = models.ManyToManyField(Subject, related_name='studies')
    collaborators = models.ManyToManyField(
        get_user_model(), related_name='studies')

    class Meta:
        verbose_name_plural = 'Studies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('research:study_detail', args=[str(self.id)])

    def generate_dicom_tree(self) -> list:
        return [subject.to_tree() for subject in self.subjects.all()]

from django.db import models


class DataSource(models.Model):
    name = models.CharField(max_length=64, blank=True)

    class Meta:
        abstract = True

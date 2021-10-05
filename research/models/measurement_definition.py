"""
Definition of the :class:`MeasurementDefinition` model.
"""
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from research.models.event import Event
from research.models.study import Study


class MeasurementDefinition(Event):
    """
    Represents an experimental measurement definition.
    """

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )

    def get_absolute_url(self):
        """
        Returns the canonical URL for this instance.

        References
        ----------
        * `get_absolute_url()`_

        .. _get_absolute_url():
           https://docs.djangoproject.com/en/3.0/ref/models/instances/#get-absolute-url

        Returns
        -------
        str
            URL
        """

        return reverse("research:measurement-detail", args=[str(self.id)])

    def get_instance_set(self) -> models.QuerySet:
        """
        Returns a queryset of collected measurements associated with this
        measurements definition.

        Returns
        -------
        models.QuerySet
            Collected data instances
        """
        if self.content_type:
            DataModel = self.content_type.model_class()
            return DataModel.objects.filter(measurement=self)

    def query_associated_studies(self) -> models.QuerySet:
        return Study.objects.filter(
            id__in=self.procedure_set.values_list("study")
        )

    @property
    def instance_set(self) -> models.QuerySet:
        """
        Returns a queryset of collected measurements associated with this
        measurements definition.

        Returns
        -------
        models.QuerySet
            Collected data instances

        See Also
        --------
        * :meth:`get_instance_set`
        """
        return self.get_instance_set()

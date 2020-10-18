"""
Definition of the :class:`~research.models.MeasurementDefinition` model.
"""

from django.db import models
from django.urls import reverse
from research.models.event import Event


class MeasurementDefinition(Event):
    """
    Represents an experimental measurement definition.
    """

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


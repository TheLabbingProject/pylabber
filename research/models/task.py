"""
Definition of the :class:`~research.models.task.Task` model.
"""

from research.models.event import Event
from django.urls import reverse


class Task(Event):
    """
    Represents an experimental task.
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

        return reverse("research:task-detail", args=[str(self.id)])


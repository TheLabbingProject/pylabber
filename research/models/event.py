"""
Definition of the :class:`Event` model.
"""
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel
from model_utils.managers import InheritanceManager


class Event(TitleDescriptionModel):
    """
    Represents an event as a part of a procedure.
    """

    objects = InheritanceManager()

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return self.title

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

        return reverse("research:event-detail", args=[str(self.id)])

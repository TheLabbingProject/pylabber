"""
Definition of the :class:`Procedure` model.
"""

from django.db import models
from django.urls import reverse
from research.models.event import Event
from research.models.procedure_step import ProcedureStep
from django_extensions.db.models import TitleDescriptionModel


class Procedure(TitleDescriptionModel):
    """
    Represents a procedure.
    """

    #: Represents an ordered list of events in a procedure.
    events = models.ManyToManyField(Event, through="research.ProcedureStep")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}|{self.description}"

    def add_event(self, event: Event, index: int = None):
        """
        Performs an event addition.
        """

        ProcedureStep.objects.create(index=index, event=event, procedure=self)

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

        return reverse("research:procedure-detail", args=[str(self.id)])


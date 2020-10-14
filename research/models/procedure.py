"""
Definition of the :class:`~research.models.procedure.Procedure` model.
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
    #: A variable to order the events in the list.
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}|{self.description}"

    @property
    def curr_index(self):
        """
        Calculates the relevant index for the current added event.
        """

        self.index += 1
        return self.index

    def add_event(self, event: Event):
        """
        Performs an event addition, 
        using the curr_index and the maximum of indices.
        """

        if len(self.events.all()) > 0:
            (max_index,) = max(self.events.values_list("procedurestep__index"))
            self.index = max_index + 1
            curr_index = self.index
        else:
            curr_index = self.curr_index
        ProcedureStep.objects.create(
            index=curr_index, event=event, procedure=self
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

        return reverse("research:procedure-detail", args=[str(self.id)])


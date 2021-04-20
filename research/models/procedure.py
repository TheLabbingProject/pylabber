"""
Definition of the :class:`Procedure` model.
"""

from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel
from research.models.event import Event
from research.models.managers.procedure import ProcedureManager
from research.models.procedure_step import ProcedureStep


class Procedure(TitleDescriptionModel):
    """
    Represents an experimental procedure.
    """

    #: Represents an ordered list of events in a procedure.
    events = models.ManyToManyField(Event, through="research.ProcedureStep")

    objects = ProcedureManager.as_manager()

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """

        return self.title

    def add_event(self, event: Event, index: int = None):
        """
        Performs an event addition.
        """

        index = self.max_index + 1 if index is None else index
        return ProcedureStep.objects.create(
            index=index, event=event, procedure=self
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

    @property
    def max_index(self) -> int:
        """
        Returns the maximal
        :attr:`~research.models.procedure_step.ProcedureStep.index` field value
        of any associated
        :class:`~research.models.procedure_step.ProcedureStep` instances. If
        there aren't any, returns -1.

        Returns
        -------
        int
            Maximal step index, or -1
        """

        last_step = self.step_set.order_by("-index").first()
        return last_step.index if last_step else -1

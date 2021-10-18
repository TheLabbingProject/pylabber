"""
Definition of the :class:`ProcedureStep` model.
"""
from django.db import IntegrityError, models
from django.urls import reverse
from research.models.managers.procedure_step import ProcedureStepManager


class ProcedureStep(models.Model):
    """
    Represents an item in the :class:`~research.models.Event` list of
    :class:`~research.models.Procedure` model.
    """

    #: An index to indicate the location in the procedure's ordered list.
    index = models.PositiveIntegerField()

    #: The event related to the current item.
    event = models.ForeignKey("research.Event", on_delete=models.CASCADE)

    #: The procedure related to this item.
    procedure = models.ForeignKey(
        "research.Procedure", on_delete=models.PROTECT, related_name="step_set"
    )

    objects = ProcedureStepManager.as_manager()

    class Meta:
        ordering = "procedure", "index"
        unique_together = ("procedure", "index")

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """
        return f"[{self.procedure.title}] #{self.index}:\t{self.event.title}"

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide automatic index management. By default will assign an
        incrementing index value.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """
        # If no index is assigned, append to the procedure as a new last step.
        if self.index is None:
            self.index = self.procedure.max_index + 1
        # elif self.index > self.procedure.max_index + 1:
        #     self.index = 0
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            current_step = ProcedureStep.objects.get(
                procedure=self.procedure, index=self.index
            )
            current_step.index += 1
            current_step.save()
            super().save(*args, **kwargs)
        # TODO: Fix automatic index management

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
        return reverse("research:procedure_step-detail", args=[str(self.id)])

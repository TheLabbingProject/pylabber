"""
Definition of the :class:`ProcedureStep`.
"""
from django.db import models
from django.urls import reverse


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
        "research.Procedure", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("index",)
        unique_together = ("procedure", "index")

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom validation.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """

        if self.index is None:
            steps = ProcedureStep.objects.filter(procedure=self.procedure)
            if steps:
                max_index = steps.order_by("-index").first().index
                self.index = max_index + 1
            else:
                self.index = 0
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            step = ProcedureStep.objects.get(
                procedure=self.procedure, index=self.index
            )
            step.index = models.F("index") + 1
            step.save()
            super().save(*args, **kwargs)

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

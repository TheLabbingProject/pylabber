"""
Definition of the :class:`~research.models.ProcedureStep`
"""
from django.db import models


class ProcedureStep(models.Model):
    """
    Represents an item in the :class:`~research.models.Event` list of :class:`~research.models.Procedure` model.
    """

    index = models.PositiveIntegerField()
    event = models.ForeignKey("research.Event", on_delete=models.CASCADE)
    procedure = models.ForeignKey(
        "research.Procedure", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("index",)

    def save(self, *args, **kwargs):
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
        if self.index == 0:
            events = self.procedure.events
            if events.all():
                max_index = max(events.values_list("index",))
                if max_index > 0:
                    self.index = max_index
            else:
                self.index = 1

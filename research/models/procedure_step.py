"""
Definition of the :class:`~research.models.ProcedureStep`
"""
from django.db import models
from django.urls import reverse


class ProcedureStep(models.Model):
    """
    Represents an item in the :class:`~research.models.Event` list of :class:`~research.models.Procedure` model.
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

"""
Signal receivers.

References
----------
* Signals_

.. _Signals:
   https://docs.djangoproject.com/en/3.0/ref/signals/
"""


from django.db.models import F, Model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from research.models.procedure_step import ProcedureStep


@receiver(post_delete, sender=ProcedureStep)
def procedure_step_post_delete_receiver(
    sender: Model, instance: ProcedureStep, using, **kwargs
) -> None:
    """
    Fix related procedure's step indices when removing a procedure step.

    Parameters
    ----------
    sender : Model
        The :class:`~research.models.procedure_step.ProcedureStep` model
    instance : ProcedureStep
        The ProcedureStep instance
    using : Any
        The database alias being used
    """

    next_steps = sender.objects.filter(
        procedure=instance.procedure, index__gt=instance.index
    )
    next_steps.update(index=F("index") - 1)

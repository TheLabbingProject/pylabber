"""
Subclasses of the :class:`~pylabber.utils.ChoiceEnum` class used to represent
raw and human-readable values for choices within the :mod:`research.models`
module.
"""
from pylabber.utils import ChoiceEnum


class Sex(ChoiceEnum):
    """
    An :class:`~enum.Enum` representing supported sex options.
    """

    M = "Male"
    F = "Female"
    U = "Other"


class Gender(ChoiceEnum):
    """
    An :class:`~enum.Enum` representing supported gender options.
    """

    CIS = "Cisgender"
    TRANS = "Transgender"
    OTHER = "Other"


class DominantHand(ChoiceEnum):
    """
    An :class:`~enum.Enum` representing supported dominant hand options.
    """

    R = "Right"
    L = "Left"
    A = "Ambidextrous"

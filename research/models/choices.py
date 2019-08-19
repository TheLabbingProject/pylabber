"""
Subclasses of the :class:`~pylabber.utils.ChoiceEnum` class used to represent
raw and human-readable values for choices within the :mod:`research.models` module.

"""


from pylabber.utils import ChoiceEnum


class Sex(ChoiceEnum):
    M = "Male"
    F = "Female"
    U = "Other"


class Gender(ChoiceEnum):
    CIS = "Cisgender"
    TRANS = "Transgender"
    OTHER = "Other"


class DominantHand(ChoiceEnum):
    R = "Right"
    L = "Left"
    A = "Ambidextrous"

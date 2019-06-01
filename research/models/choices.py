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

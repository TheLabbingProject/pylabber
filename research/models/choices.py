from pylabber.utils import ChoiceEnum


class Sex(ChoiceEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class Gender(ChoiceEnum):
    CIS = 'Cisgender'
    TRANS = 'Transgender'
    OTHER = 'Other'


class DominantHand(ChoiceEnum):
    RIGHT = 'Right'
    LEFT = 'Left'
    AMBI = 'Ambidextrous'

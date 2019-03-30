from django_dicom.models.choice_enum import ChoiceEnum


class ScanningSequence(ChoiceEnum):
    SE = "Spin Echo"
    IR = "Inversion Recovery"
    GR = "Gradient Recalled"
    EP = "Echo Planar"
    RM = "Research Mode"

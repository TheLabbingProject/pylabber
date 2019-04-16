"""
A ChoiceEnum to represent ScanningSequence_ values.

.. _ScanningSequence: https://dicom.innolitics.com/ciods/mr-image/mr-image/00180020

"""


from django_dicom.models.choice_enum import ChoiceEnum


class ScanningSequence(ChoiceEnum):
    SE = "Spin Echo"
    IR = "Inversion Recovery"
    GR = "Gradient Recalled"
    EP = "Echo Planar"
    RM = "Research Mode"

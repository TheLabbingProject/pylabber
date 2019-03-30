from django_dicom.models.choice_enum import ChoiceEnum


class SequenceVariant(ChoiceEnum):
    SK = "Segmented k-Space"
    MTC = "Magnetization Transfer Contrast"
    SS = "Steady State"
    TRSS = "Time Reversed Steady State"
    SP = "Spoiled"
    MP = "MAG Prepared"
    OSP = "Oversampling Phase"
    NONE = "None"

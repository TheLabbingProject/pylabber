"""
A list of common MRI sequences and their respective DICOM header attributes.

"""


sequences = [
    {
        "name": "MPRAGE",
        "description": "",
        "scanning_sequence": ["GR", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "name": "Localizer",
        "description": "",
        "scanning_sequence": ["GR"],
        "sequence_variant": ["SP", "OSP"],
    },
    {
        "name": "IR-EPI",
        "description": "",
        "scanning_sequence": ["EP", "IR"],
        "sequence_variant": ["SK", "SP", "MP", "OSP"],
    },
    {
        "name": "FLAIR",
        "description": "",
        "scanning_sequence": ["SE", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "name": "DWI",
        "description": "",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SP"],
    },
    {
        "name": "Resting-state fMRI",
        "description": "",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SS"],
    },
]

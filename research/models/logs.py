"""
Log message string templates for the :mod:`~research.models` module.
"""
SUBJECT_NIFTI_CONVERSION_START: str = "Starting to convert subject #{pk}'s MRI data to NIfTI..."
SUBJECT_NIFTI_CONVERSION_SUCCESS: str = "Successfully converted subject #{pk}'s MRI data to NIfTI."
SUBJECT_NIFTI_CONVERSION_FAILURE: str = "Failed to convert subject #{pk}'s MRI data to NIfTI with the following exception:\n{exception}"

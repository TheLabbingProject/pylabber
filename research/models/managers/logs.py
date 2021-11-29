"""
Log message string templates for the :mod:`~research.models.managers` module.
"""
SUBJECT_SET_BIDS_BUILD_START: str = "Starting to build BIDS directories for {count} subjects..."
SUBJECT_SET_BIDS_BUILD_SUCCESS: str = "Successfully completed BIDS directory build for {count} subjects."
SUBJECT_SET_BIDS_BUILD_FAILURE: str = "Failed to complete BIDS directory build after {n_built}/{n_total} subjects with the following exception:\n{exception}"

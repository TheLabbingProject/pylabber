from django.db.models import Count, F

MRI_SESSION_COUNT_KEY: str = "n_mri_session_subjects"
MRI_SESSIONS_QUERY: str = "procedures__events__measurementdefinition__mri_session_set__subject"  # noqa: E501
MRI_SCAN_COUNT_KEY: str = "n_mri_scan_subjects"
MRI_SCAN_QUERY: str = "group__mri_scan_set__session__subject"
SUBJECT_COUNT_KEY: str = "n_subjects"

STUDY_SUBJECTS_AGGREGATION = {
    MRI_SESSION_COUNT_KEY: Count(MRI_SESSIONS_QUERY, distinct=True,),
    MRI_SCAN_COUNT_KEY: Count(MRI_SCAN_QUERY, distinct=True),
}

STUDY_SUBJECTS_ANNOTATION = {
    SUBJECT_COUNT_KEY: F(MRI_SESSION_COUNT_KEY) + F(MRI_SCAN_COUNT_KEY)
}

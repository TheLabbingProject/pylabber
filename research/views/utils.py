from django.db.models import Max, Min

CSV_CONTENT_TYPE: str = "text/csv"

STUDY_AGGREGATIONS = {
    "nSubjectsMin": Min("n_subjects"),
    "nSubjectsMax": Max("n_subjects"),
}

from django.db.models import Min, Max


STUDY_AGGREGATIONS = {
    "nSubjectsMin": Min("n_subjects"),
    "nSubjectsMax": Max("n_subjects"),
}

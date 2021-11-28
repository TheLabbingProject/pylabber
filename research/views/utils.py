from bs4 import BeautifulSoup
from django.db.models import Max, Min

CSV_CONTENT_TYPE: str = "text/csv"

STUDY_AGGREGATIONS = {
    "nSubjectsMin": Min("n_subjects"),
    "nSubjectsMax": Max("n_subjects"),
}

DEFAULT_DESTINATION_ID = "bk-app"


def fix_bokeh_script(
    html: str, destination_id: str = DEFAULT_DESTINATION_ID
) -> str:
    soup = BeautifulSoup(html, features="lxml")
    element = soup(["script"])[0]
    random_id = element.attrs["id"]
    script = element.contents[0]
    return script.replace(random_id, destination_id)

import pandas as pd

from django.conf import settings


def read_subject_table() -> pd.DataFrame:
    return pd.read_excel(
        settings.RAW_SUBJECT_TABLE_PATH,
        sheet_name="Subjects",
        header=[0, 1],
        converters={("Raw", "Patient ID"): str},
    )


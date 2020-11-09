import pandas as pd

from django.conf import settings


def read_subject_table() -> pd.DataFrame:
    return pd.read_excel(
        settings.RAW_SUBJECT_TABLE_PATH,
        sheet_name="Subjects",
        header=[0, 1],
        converters={
            ("Raw", "Patient ID"): str,
            ("Questionnaire", "Questionnaire"): str,
        },
    )


def merge_subject_and_questionnaire_data(
    subject_data, questionnaire_data
) -> pd.DataFrame:
    return pd.merge(
        subject_data,
        questionnaire_data,
        how="inner",
        left_on=subject_data["Questionnaire", "Questionnaire"],
        right_on=questionnaire_data.index,
    )


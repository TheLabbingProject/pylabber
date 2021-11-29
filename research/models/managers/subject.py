import logging

import pandas as pd
from bokeh.layouts import layout
from bokeh.models import Column
from bokeh.plotting import Figure
from django.db import models
from django.db.models import Count, Max
from django_dicom.models.patient import Patient
from research.models.managers import logs
from research.plots.subject import (
    plot_bokeh_date_of_birth,
    plot_bokeh_dominant_hand_pie,
    plot_bokeh_sex_pie,
)
from tqdm import tqdm

#: Subject fields to include in an exported DataFrame.
DATAFRAME_FIELDS = (
    "id",
    "id_number",
    "first_name",
    "last_name",
    "sex",
    "date_of_birth",
    "dominant_hand",
)
#: Column names to use when exporting a Subject queryset as a DataFrame.
DATAFRAME_COLUMNS = (
    "ID",
    "ID Number",
    "First Name",
    "Last Name",
    "Sex",
    "Date Of Birth",
    "Dominant Hand",
)


class SubjectManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                latest_mri_session_time=Max("mri_session_set__time"),
                mri_session_count=Count("mri_session_set"),
            )
        )


class SubjectQuerySet(models.QuerySet):
    _logger = logging.getLogger("research.subject")

    def to_dataframe(self) -> pd.DataFrame:
        """
        Export the queryset as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Queryset information
        """
        df = pd.DataFrame(self.values(*DATAFRAME_FIELDS))
        df.columns = DATAFRAME_COLUMNS
        return df.set_index("ID").sort_index()

    def from_dicom_patient(self, patient: Patient) -> tuple:
        data = {
            "id_number": patient.uid,
            "first_name": patient.given_name,
            "last_name": patient.family_name,
            "date_of_birth": patient.date_of_birth,
            "sex": patient.sex,
        }
        return self.get_or_create(**data)

    def plot_bokeh_sex_pie(self) -> Figure:
        return plot_bokeh_sex_pie(self.all())

    def plot_bokeh_dominant_hand_pie(self) -> Figure:
        return plot_bokeh_dominant_hand_pie(self.all())

    def plot_bokeh_date_of_birth(self) -> Figure:
        return plot_bokeh_date_of_birth(self.all())

    def plot_summary_info(self) -> Column:
        sex_plot = self.plot_bokeh_sex_pie()
        dominant_hand_plot = self.plot_bokeh_dominant_hand_pie()
        dob_plot = self.plot_bokeh_date_of_birth()
        figure_layout = [[sex_plot, dominant_hand_plot]]
        if dob_plot is not None:
            figure_layout[0].append(dob_plot)
        return layout(figure_layout)

    def build_bids_directory(
        self,
        force: bool = False,
        persistent: bool = True,
        progressbar: bool = False,
        progressbar_position: int = 0,
    ):
        # Run chronologically in reverse.
        queryset = self.order_by("-latest_mri_session_time")
        # Log BIDS build start.
        start_log = logs.SUBJECT_SET_BIDS_BUILD_START.format(
            count=queryset.count()
        )
        self._logger.debug(start_log)
        # Create progressbar if required.
        iterator = (
            tqdm(
                queryset,
                desc="Subjects",
                unit="subject",
                position=progressbar_position,
            )
            if progressbar
            else queryset
        )
        n_built = 0
        # Iterate subjects and build BIDS directories.
        try:
            for subject in iterator:
                subject.build_bids_directory(
                    force=force,
                    persistent=persistent,
                    progressbar=progressbar,
                    progressbar_position=progressbar_position + 1,
                )
                n_built += 1
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SUBJECT_SET_BIDS_BUILD_FAILURE.format(
                n_built=n_built, n_total=queryset.count(), exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log successful BIDS build.
            success_log = logs.SUBJECT_SET_BIDS_BUILD_SUCCESS.format(
                count=queryset.count()
            )
            self._logger.debug(success_log)

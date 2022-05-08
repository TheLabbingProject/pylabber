"""
Definition of the :class:`Subject` model.
"""
import logging
from pathlib import Path
from typing import Iterable, Union

import pandas as pd
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, QuerySet
from django.urls import reverse
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.integer_input_definition import (
    IntegerInputDefinition,
)
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from django_analyses.models.input.types.integer_input import IntegerInput
from django_analyses.models.input.types.list_input import ListInput
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel
from django_mri.utils import get_bids_dir
from pylabber.utils import CharNullField
from questionnaire_reader import QuestionnaireReader
from research.models import logs
from research.models.choices import DominantHand, Gender, Sex
from research.models.group import Group
from research.models.managers.subject import SubjectManager, SubjectQuerySet
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure
from research.models.validators import not_future
from research.utils.custom_attributes_processor import (
    CustomAttributesProcessor,
)
from research.utils.subject_table import (
    merge_subject_and_questionnaire_data,
    read_subject_table,
)


class Subject(TimeStampedModel):
    """
    Represents a single research subject. Any associated data model should be
    associated with this model.
    """

    #: Some representative ID number unique to this subject.
    id_number = CharNullField(
        max_length=64, unique=True, blank=True, null=True
    )

    #: Subject's first name.
    first_name = models.CharField(max_length=64, blank=True, null=True)

    #: Subject's last name.
    last_name = models.CharField(max_length=64, blank=True, null=True)

    #: Subject's date of birth.
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        blank=True,
        null=True,
        validators=[not_future],
    )

    #: Subject's dominant hand.
    dominant_hand = models.CharField(
        max_length=5, choices=DominantHand.choices(), blank=True, null=True
    )

    #: Subject's sex.
    sex = models.CharField(
        max_length=6, choices=Sex.choices(), blank=True, null=True
    )

    #: Subject's gender.
    gender = models.CharField(
        max_length=5, choices=Gender.choices(), blank=True, null=True
    )

    #: Custom attributes dictionary.
    custom_attributes = models.JSONField(blank=True, default=dict)

    objects = SubjectManager.from_queryset(SubjectQuerySet)()

    BIDS_DIR_TEMPLATE: str = "sub-{pk}"

    _logger = logging.getLogger("research.subject")

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        return f"Subject #{self.id}"

    def get_absolute_url(self):
        """
        Returns the canonical URL for this instance.

        References
        ----------
        * `get_absolute_url()`_

        .. _get_absolute_url():
           https://docs.djangoproject.com/en/3.0/ref/models/instances/#get-absolute-url

        Returns
        -------
        str
            URL
        """
        return reverse("research:subject-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        process custom attributes.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """
        custom_attributes_processor = CustomAttributesProcessor()
        custom_attributes_processor.validate(self.custom_attributes)
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        """
        Returns a formatted string with the subject's full name (first name
        and then last name).

        Returns
        -------
        str
            Subject's full name
        """
        return f"{self.first_name} {self.last_name}"

    def query_measurements(self) -> models.QuerySet:
        measurement_ids = self.mri_session_set.values("measurement")
        return MeasurementDefinition.objects.filter(id__in=measurement_ids)

    def query_procedures(self) -> models.QuerySet:
        measurements = self.query_measurements()
        procedure_ids = measurements.values("procedure")
        return Procedure.objects.filter(id__in=procedure_ids)

    def query_study_groups(self) -> models.QuerySet:
        group_ids = self.mri_session_set.values("scan__study_groups")
        return Group.objects.filter(id__in=group_ids)

    def query_studies(self) -> models.QuerySet:
        """
        Returns a queryset of :class:`~research.models.study.Study` instances
        this subject has data associated with.

        Returns
        -------
        models.QuerySet
            Associated studies
        """
        return self.mri_session_set.query_studies()

    def query_run_set(self) -> models.QuerySet:
        content_type = ContentType.objects.get_for_model(self)
        list_input_definitions = ListInputDefinition.objects.filter(
            content_type=content_type
        )
        integer_input_definitions = IntegerInputDefinition.objects.filter(
            content_type=content_type
        )
        list_inputs = ListInput.objects.filter(
            Q(definition__in=list_input_definitions)
            & (
                Q(definition__element_type="INT", value__contains=self.id)
                | Q(
                    definition__element_type="STR",
                    value__contains=str(self.id),
                )
            )
        )
        integer_inputs = IntegerInput.objects.filter(
            definition__in=integer_input_definitions, value=self.id
        )
        run_ids = set(list_inputs.values_list("run", flat=True)) | set(
            integer_inputs.values_list("run", flat=True)
        )
        runs = Run.objects.none()
        for mri_session in self.mri_session_set.all():
            runs |= mri_session.query_run_set()
        return Run.objects.filter(id__in=run_ids) | runs

    def get_personal_information(self) -> pd.Series:
        """
        Temporary method to use an external table to retrieve subject
        personal information.

        Returns
        -------
        pd.Series
            Subject personal information
        """
        subject_table = read_subject_table()
        subject_table["Questionnaire", "Questionnaire"].fillna(
            "", inplace=True
        )
        this_subject = (
            subject_table["Anonymized", "Patient ID"] == self.id_number
        )
        return subject_table[this_subject]

    def get_raw_information(self) -> pd.Series:
        """
        Temporary method to use an external table to retrieve subject
        information.

        Returns
        -------
        pd.Series
            Subject information
        """
        this_subject = self.get_personal_information()
        return this_subject["Raw"].squeeze()

    def get_questionnaire_data(self):
        """
        A method to link between a subject to it's questionnaire data.

        Returns
        -------
        pd.Series
            Subject and Questionnaire information.
        """
        # Getting the questionnaire data from the sheets document.
        questionnaire = QuestionnaireReader(
            path=settings.QUESTIONNAIRE_DATA_PATH
        ).data

        subject_data = self.get_personal_information()
        # Merging tables to get the questionnaire data.
        output = merge_subject_and_questionnaire_data(
            subject_data, questionnaire
        )
        return output[self.id_number == output["Anonymized", "Patient ID"]]

    def build_bids_directory(
        self,
        force: bool = False,
        persistent: bool = True,
        progressbar: bool = False,
        progressbar_position: int = 0,
    ):
        # Log start.
        start_log = logs.SUBJECT_NIFTI_CONVERSION_START.format(pk=self.id)
        self._logger.debug(start_log)
        # Convert MRI sessions to NIfTI.
        try:
            self.mri_session_set.convert_to_nifti(
                force=force,
                persistent=persistent,
                progressbar=progressbar,
                progressbar_position=progressbar_position,
            )
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SUBJECT_NIFTI_CONVERSION_FAILURE.format(
                pk=self.id, exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log successful conversion.
            success_log = logs.SUBJECT_NIFTI_CONVERSION_SUCCESS.format(
                pk=self.id
            )
            self._logger.debug(success_log)

    def get_bids_directory(self) -> Path:
        bids_root = get_bids_dir()
        subject_dir_name = self.BIDS_DIR_TEMPLATE.format(pk=self.id)
        return bids_root / subject_dir_name

    def query_scores(
        self,
        analysis: Union[Analysis, Iterable[Analysis]] = None,
        analysis_title: Union[str, Iterable[str]] = None,
        analysis_version: Union[
            AnalysisVersion, Iterable[AnalysisVersion]
        ] = None,
        analysis_version_title: Union[str, Iterable[str]] = None,
        atlas=None,
        atlas_title: Union[str, Iterable[str]] = None,
        metric=None,
        metric_title: Union[str, Iterable[str]] = None,
        region=None,
        region_title: Union[str, Iterable[str]] = None,
        region_index: Union[int, Iterable[int]] = None,
        hemisphere: str = None,
    ) -> QuerySet:
        runs = self.query_run_set()
        if isinstance(analysis, Analysis):
            runs = runs.filter(analysis_version__analysis=analysis)
        elif isinstance(analysis, Iterable):
            runs = runs.filter(analysis_version__analysis__in=analysis)
        elif isinstance(analysis_title, str):
            runs = runs.filter(
                analysis_version__analysis__title=analysis_title
            )
        elif isinstance(analysis_title, Iterable):
            runs = runs.filter(
                analysis_version__analysis__title__in=analysis_title
            )
        if isinstance(analysis_version, AnalysisVersion):
            runs = runs.filter(analysis_version=analysis_version)
        elif isinstance(analysis_version, Iterable):
            runs = runs.filter(analysis_version__in=analysis_version)
        elif isinstance(analysis_version_title, str):
            runs = runs.filter(analysis_version__title=analysis_version_title)
        elif isinstance(analysis_version_title, Iterable):
            runs = runs.filter(
                analysis_version__title__in=analysis_version_title
            )
        Score = apps.get_model("django_mri", "score")
        scores = Score.objects.filter(run__in=runs)
        if isinstance(atlas, Iterable):
            scores = scores.filter(region__atlas__in=atlas)
        elif atlas is not None:
            scores = scores.filter(region__atlas=atlas)
        elif isinstance(atlas_title, str):
            scores = scores.filter(region__atlas__title=atlas_title)
        elif isinstance(atlas_title, Iterable):
            scores = scores.filter(region__atlas__title__in=atlas_title)
        if isinstance(metric, Iterable):
            scores = scores.filter(metric__in=metric)
        elif metric is not None:
            scores = scores.filter(metric=metric)
        elif isinstance(metric_title, str):
            scores = scores.filter(metric__title=metric_title)
        elif isinstance(metric_title, Iterable):
            scores = scores.filter(metric__title__in=metric_title)
        if isinstance(region, Iterable):
            scores = scores.filter(region__in=region)
        elif region is not None:
            scores = scores.filter(region=region)
        elif isinstance(region_title, str):
            scores = scores.filter(region__title=region_title)
        elif isinstance(region_title, Iterable):
            scores = scores.filter(region__title__in=region_title)
        elif isinstance(region_index, int):
            scores = scores.filter(region__index=region_index)
        elif isinstance(region_index, Iterable):
            scores = scores.filter(region__index__in=region_index)
        if hemisphere is not None:
            scores = scores.filter(region__hemisphere=hemisphere)
        return scores

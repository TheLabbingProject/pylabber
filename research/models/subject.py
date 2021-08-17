"""
Definition of the :class:`Subject` model.
"""
import itertools

import pandas as pd
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from pylabber.utils import CharNullField
from questionnaire_reader import QuestionnaireReader
from research.models.choices import DominantHand, Gender, Sex
from research.models.group import Group
from research.models.managers.subject import SubjectManager, SubjectQuerySet
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure
from research.models.study import Study
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

        custom_attributes_processor = CustomAttributesProcessor(
            self.custom_attributes
        )
        custom_attributes_processor.validate()
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

    def query_studies(self, id_only: bool = False) -> models.QuerySet:
        """
        Returns a queryset of :class:`~research.models.study.Study` instances
        this subject has data associated with.

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of IDs instead of a queryset, defaults to
            False

        Returns
        -------
        models.QuerySet
            Associated studies
        """
        group_query = models.Q(
            id__in=self.mri_session_set.values("scan__study_groups__study")
        )
        procedure_query = models.Q(
            id__in=self.mri_session_set.values("measurement__procedure__study")
        )
        return Study.objects.filter(group_query | procedure_query)

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

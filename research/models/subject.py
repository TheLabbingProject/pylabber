"""
Definition of the :class:`~research.models.subject.Subject` model.
"""

import pandas as pd

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from pylabber.utils import CharNullField
from research.models.managers.subject import SubjectQuerySet
from research.utils.custom_attributes_processor import (
    CustomAttributesProcessor,
)
from research.utils.subject_table import read_subject_table
from research.models.choices import Sex, Gender, DominantHand
from research.models.validators import not_future


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
    custom_attributes = JSONField(blank=True, default=dict)

    objects = SubjectQuerySet.as_manager()

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

        return reverse("research:subject_detail", args=[str(self.id)])

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

    def get_raw_information(self) -> pd.Series:
        """
        Temporary method to use an external table to retrieve subject
        information.

        Returns
        -------
        pd.Series
            Subject information
        """

        subject_table = read_subject_table()
        this_subject = (
            subject_table["Anonymized", "Patient ID"] == self.id_number
        )
        return subject_table[this_subject]["Raw"].squeeze()

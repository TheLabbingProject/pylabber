"""
Definition of the :class:`SubjectFilter` class.
"""
from django.db.models import Q
from django_dicom.models.patient import Patient
from django_filters import rest_framework as filters
from django_mri.models.scan import Scan
from research.models.subject import Subject

from utils.lookup_choices import DEFUALT_LOOKUP_CHOICES


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class SubjectFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.subject.Subject` model.
    """

    born_after_date = filters.DateFilter("date_of_birth", lookup_expr="gte")
    born_before_date = filters.DateFilter("date_of_birth", lookup_expr="lte")
    first_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    last_name = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    dicom_patient = filters.NumberFilter(
        method="filter_by_dicom_patient", label="DICOM Patient ID"
    )
    sex = filters.CharFilter(method="filter_nullable_charfield")
    gender = filters.CharFilter(method="filter_nullable_charfield")
    dominant_hand = filters.CharFilter(method="filter_nullable_charfield")
    id_number = filters.LookupChoiceFilter(
        lookup_choices=DEFUALT_LOOKUP_CHOICES
    )
    studies = NumberInFilter(method="filter_by_studies", label="Studies")

    class Meta:
        model = Subject
        fields = (
            "id",
            "first_name",
            "last_name",
            "sex",
            "gender",
            "born_after_date",
            "born_before_date",
            "dominant_hand",
            "dicom_patient",
            "id_number",
        )

    def filter_by_dicom_patient(self, queryset, name, value):
        """
        Find the subject that represents a particular DICOM
        :class:`~django_dicom.models.patient.Patient` instance.

        Parameters
        ----------
        queryset : django.db.models.QuerySet
            The :class:`~research.models.subject.Subject` queryset to filter.
        name : str
            The name of the model field to filter on.
        value : int
            DICOM :class:`~django_dicom.models.patient.Patient` ID.
        """
        if not value:
            return queryset

        dicom_patient = Patient.objects.get(id=value)
        mri_scans = Scan.objects.filter(
            dicom__in=dicom_patient.series_set.all()
        )
        subject_ids = set(
            mri_scans.order_by("session__subject").values_list(
                "session__subject", flat=True
            )
        )
        return queryset.filter(id=subject_ids.pop())

    def filter_nullable_charfield(self, queryset, name, value):
        if value == "null":
            return queryset.filter(
                Q(**{f"{name}__isnull": True}) | Q(**{f"{name}__exact": ""})
            )
        return queryset.filter(**{name: value})

    def filter_by_studies(self, queryset, name, value):
        ids = [
            subject.id
            for subject in queryset
            if any(
                study_id in subject.query_studies(id_only=True)
                for study_id in value
            )
        ]
        return queryset.filter(id__in=ids)

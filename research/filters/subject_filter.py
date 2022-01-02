"""
Definition of the :class:`SubjectFilter` class.
"""
from django.db.models import Prefetch, Q
from django_dicom.models.patient import Patient
from django_filters import rest_framework as filters
from django_mri.models.scan import Scan
from pylabber.utils.filters import DEFUALT_LOOKUP_CHOICES, NumberInFilter
from research.models.study import Study
from research.models.subject import Subject

MEASUREMENT_DEFINITION_QUERY: str = "mri_session_set__measurement__in"
PROCEDURE_QUERY: str = "mri_session_set__measurement__procedure__in"
STUDY_BY_PROCEDURE_QUERY: str = "mri_session_set__measurement__procedure__study__in"  # noqa: E501
STUDY_GROUP_QUERY: str = "mri_session_set__scan__study_groups__in"
STUDY_BY_GROUP_QUERY: str = "mri_session_set__scan__study_groups__study__in"


class SubjectFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~research.models.subject.Subject` model.
    """

    pk = filters.LookupChoiceFilter(lookup_choices=DEFUALT_LOOKUP_CHOICES)
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
    procedure = NumberInFilter(
        method="filter_by_procedure", label="Procedures"
    )
    measurement = NumberInFilter(
        method="filter_by_measurement", label="Measurement definitions"
    )
    study_group = NumberInFilter(
        method="filter_by_study_group", label="Study group"
    )
    study = NumberInFilter(method="filter_by_studies", label="Studies")
    mri_session_time = filters.DateTimeFromToRangeFilter(
        field_name="mri_session_set__time"
    )
    # TODO: Finish filters for measurement definition and group.

    class Meta:
        model = Subject
        fields = (
            "pk",
            "first_name",
            "last_name",
            "sex",
            "gender",
            "born_after_date",
            "born_before_date",
            "dominant_hand",
            "dicom_patient",
            "id_number",
            "mri_session_time",
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
        if len(subject_ids) == 1:
            return queryset.filter(id=subject_ids.pop())
        return queryset.none()

    def filter_nullable_charfield(self, queryset, name, values):
        if isinstance(values, str):
            values = values.split(",")
            return self.filter_nullable_charfield(queryset, name, values)
        q = Q()
        for value in values:
            if value == "null":
                q |= Q(**{f"{name}__isnull": True}) | Q(
                    **{f"{name}__exact": ""}
                )
            q |= Q(**{name: value})
        return queryset.filter(q)

    def filter_by_procedure(self, queryset, name, value):
        return queryset.filter(**{PROCEDURE_QUERY: value})

    def filter_by_measurement(self, queryset, name, value):
        return queryset.filter(**{MEASUREMENT_DEFINITION_QUERY: value})

    def filter_by_study_group(self, queryset, name, value):
        return queryset.filter(**{STUDY_GROUP_QUERY: value})

    def filter_by_studies(self, queryset, name, value):
        study_subjects = Study.objects.filter(
            id__in=value
        ).query_associated_subjects()
        return queryset & study_subjects

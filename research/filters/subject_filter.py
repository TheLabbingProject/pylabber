from django_dicom.models.patient import Patient
from django_mri.models.scan import Scan
from django_filters import rest_framework as filters
from research.models.subject import Subject


class SubjectFilter(filters.FilterSet):
    """
    Provides useful filtering options for the :class:`~research.models.subject.Subject`
    model.
    
    """

    born_after_date = filters.DateFilter("date_of_birth", lookup_expr="gte")
    born_before_date = filters.DateFilter("date_of_birth", lookup_expr="lte")
    first_name = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    last_name = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    dicom_patient = filters.NumberFilter(method="filter_by_dicom_patient")

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
        mri_scans = Scan.objects.filter(dicom__in=dicom_patient.series_set.all())
        subject_ids = set(
            mri_scans.order_by("subject").values_list("subject", flat=True)
        )
        return queryset.filter(id=subject_ids.pop())


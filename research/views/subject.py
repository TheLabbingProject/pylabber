from django_dicom.models.patient import Patient
from django_mri.models.scan import Scan
from pylabber.views.defaults import DefaultsMixin
from research.filters.subject_filter import SubjectFilter
from research.models.subject import Subject
from research.serializers.subject import SubjectSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.subject.Subject` instances
    to be viewed or edited.

    """

    filter_class = SubjectFilter
    queryset = Subject.objects.order_by("-id").all()
    serializer_class = SubjectSerializer

    @action(detail=True, methods=["GET"])
    def by_dicom_patient(self, request, patient_id: int = None):
        dicom_patient = Patient.objects.get(id=patient_id)
        mri_scans = Scan.objects.filter(dicom__in=dicom_patient.series_set.all())
        subject_ids = set(
            mri_scans.order_by("subject").values_list("subject", flat=True)
        )
        if len(subject_ids) == 1:
            subject = Subject.objects.get(id=subject_ids.pop())
            serializer = SubjectSerializer(subject, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif len(subject_ids) > 1:
            return Response(
                {"message": "Subject ID for the given patient's scan is not unique!"},
                status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"message": "No subject found!"}, status=status.HTTP_204_NO_CONTENT
            )

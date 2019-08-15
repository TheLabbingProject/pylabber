from django_dicom.models.patient import Patient
from django_mri.models.scan import Scan
from django_filters.rest_framework import DjangoFilterBackend
from research.filters.subject_filter import SubjectFilter
from research.models.group import Group
from research.models.laboratory import Laboratory
from research.models.study import Study
from research.models.subject import Subject
from research.serializers.group_serializer import GroupSerializer, GroupReadSerializer
from research.serializers.laboratory_serializer import LaboratorySerializer
from research.serializers.study_serializer import StudySerializer
from research.serializers.subject_serializer import SubjectSerializer
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class DefaultsMixin:
    """
    Default settings for view authentication, permissions, filtering and pagination.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows studies to be viewed or edited.
    
    """

    pagination_class = StandardResultsSetPagination
    queryset = Study.objects.all()
    serializer_class = StudySerializer


class LaboratoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows studies to be viewed or edited.
    
    """

    pagination_class = StandardResultsSetPagination
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows subjects to be viewed or edited.
    
    """

    filter_class = SubjectFilter
    pagination_class = StandardResultsSetPagination
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


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows study groups to be viewed or edited.
    
    """

    queryset = Group.objects.order_by("id").all()
    # serializer_class = GroupSerializer
    filter_fields = ("study__id", "study__title")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GroupReadSerializer
        return GroupSerializer

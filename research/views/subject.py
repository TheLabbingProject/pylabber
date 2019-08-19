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

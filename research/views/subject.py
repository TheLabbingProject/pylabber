"""
Definition of the :class:`SubjectViewSet` class.
"""
from typing import Callable, Dict

from accounts.tasks import export_subject_mri_data
from bokeh.client import pull_session
from bokeh.embed import server_session
from bs4 import BeautifulSoup
from django.db.models import Q
from django.http import HttpResponse
from pylabber.views.defaults import DefaultsMixin
from research.filters.subject_filter import SubjectFilter
from research.models.subject import Subject
from research.serializers.subject import (
    AdminSubjectSerializer,
    SubjectSerializer,
)
from research.views.utils import CSV_CONTENT_TYPE
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

BOKEH_URL = "http://localhost:5006/date_of_birth"

DATA_EXPORT_HANDLERS: Dict[str, Callable] = {
    "mri": export_subject_mri_data.delay
}


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.subject.Subject`
    instances to be viewed or edited.
    """

    filter_class = SubjectFilter
    queryset = Subject.objects.order_by("-latest_mri_session_time")
    ordering_fields = (
        "id",
        "id_number",
        "first_name",
        "last_name",
        "date_of_birth",
        "sex",
        "dominant_hand",
        "created",
        "modified",
        "latest_mri_session_time",
        "mri_session_count",
    )

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminSubjectSerializer
        return SubjectSerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        queryset = super().filter_queryset(queryset)
        if user.is_superuser:
            return queryset
        procedure_query = Q(
            mri_session_set__measurement__procedure__study__collaborators=user
        )
        group_query = Q(
            mri_session_set__scan__study_groups__study__collaborators=user
        )
        return queryset.filter(procedure_query | group_query)

    @action(detail=False, methods=["POST"])
    def export_files(self, request):
        try:
            export_destination_id = request.data.pop("export_destination_id")
            instance_id = request.data.pop("instance_id")
        except KeyError:
            Response(status.HTTP_400_BAD_REQUEST)
        else:
            for data_type, parameters in request.data.items():
                handler = DATA_EXPORT_HANDLERS.get(data_type)
                if handler:
                    handler(export_destination_id, instance_id, **parameters)
            return Response(status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def to_csv(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        df = queryset.to_dataframe()
        response = HttpResponse(
            content_type=CSV_CONTENT_TYPE,
            headers={
                "Content-Disposition": 'attachment; filename="subjects.csv"'
            },
        )
        df.to_csv(path_or_buf=response)
        return response

    @action(detail=False, methods=["GET"])
    def plot(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        with pull_session(url=BOKEH_URL) as session:
            script = server_session(session_id=session.id, url=BOKEH_URL)
        return Response(script)

    @action(detail=False, methods=["GET"])
    def plot_script(self, request, *args, **kwargs):
        destination_id = request.GET.get("id", "bk-plot")
        with pull_session(url=BOKEH_URL) as session:
            script = server_session(session_id=session.id, url=BOKEH_URL)
            soup = BeautifulSoup(script, features="lxml")
            element = soup(["script"])[0]
            random_id = element.attrs["id"]
            script = element.contents[0]
            script = script.replace(random_id, destination_id)
        return HttpResponse(script, content_type="text/javascript")

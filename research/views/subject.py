from bokeh.client import pull_session
from bokeh.embed import server_session
from bs4 import BeautifulSoup
from django.http import HttpResponse
from pylabber.views.defaults import DefaultsMixin
from research.filters.subject_filter import SubjectFilter
from research.models.subject import Subject
from research.serializers.subject import SubjectSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


BOKEH_URL = "http://localhost:5006/date_of_birth"


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.subject.Subject` instances
    to be viewed or edited.

    """

    filter_class = SubjectFilter
    queryset = Subject.objects.order_by("-id").all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        # TODO: Implement filtering according to the user's collaborations
        return Subject.objects.all()

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

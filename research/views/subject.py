from pylabber.views.defaults import DefaultsMixin
from research.filters.subject_filter import SubjectFilter
from research.models.subject import Subject
from research.serializers.subject import SubjectSerializer
from rest_framework import viewsets


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

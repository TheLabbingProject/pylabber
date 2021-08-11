from pylabber.views.defaults import DefaultsMixin
from research.filters.study_filter import StudyFilter
from research.models.study import Study
from research.serializers.study import StudySerializer
from rest_framework import viewsets


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.study.Study` instances to
    be viewed or edited.

    """

    filter_class = StudyFilter
    queryset = Study.objects.order_by("title").all()
    serializer_class = StudySerializer

    def filter_queryset(self, queryset):
        """
        Filters the returned study queryset according to the user's
        collaborations.

        Parameters
        ----------
        queryset : QuerySet
            Base `Study` queryset

        Returns
        -------
        QuerySet
            Studies in which the user is a collaborator
        """
        user = self.request.user
        if user.is_superuser:
            return super().filter_queryset(queryset)
        return queryset.filter(collaborators__in=[user])

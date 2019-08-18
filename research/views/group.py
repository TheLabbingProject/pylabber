from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets
from research.models.group import Group
from research.serializers.group import GroupSerializer, GroupReadSerializer


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows study groups to be viewed or edited.
    
    """

    pagination_class = StandardResultsSetPagination
    queryset = Group.objects.order_by("id").all()
    filter_fields = ("study__id", "study__title")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GroupReadSerializer
        return GroupSerializer

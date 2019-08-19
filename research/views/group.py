from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets
from research.models.group import Group
from research.serializers.group import GroupSerializer, GroupReadSerializer


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.group.Group` instances
    to be viewed or edited.
    
    """

    queryset = Group.objects.order_by("id").all()
    filter_fields = ("study__id", "study__title")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GroupReadSerializer
        return GroupSerializer

from accounts.serializers.group import GroupSerializer
from django.contrib.auth.models import Group
from pylabber.views.defaults import DefaultsMixin
from rest_framework import viewsets


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~accounts.models.group.Group` instances to
    be viewed or edited.

    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

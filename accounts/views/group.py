from accounts.serializers.group import GroupSerializer
from django.contrib.auth.models import Group
from pylabber.views.defaults import DefaultsMixin
from pylabber.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

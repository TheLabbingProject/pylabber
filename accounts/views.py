from django.contrib.auth.models import Group
from accounts.models import Profile, User
from accounts.serializers import GroupSerializer, ProfileSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


class DefaultsMixin:
    """
    Default settings for view authentication, permissions, filtering and pagination.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows user profles to be viewed or edited.
    """

    queryset = User.objects.all().order_by("date_joined")
    serializer_class = UserSerializer


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows user profles to be viewed or edited.
    """

    queryset = Profile.objects.all().order_by("-user__date_joined")
    serializer_class = ProfileSerializer

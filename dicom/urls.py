from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.InstanceListView.as_view(),
        name='instance_list',
    ),
    path(
        'new/',
        views.InstancesCreateView.as_view(),
        name='instances_create',
    ),
    path(
        '<int:pk>/',
        views.InstanceDetailView.as_view(),
        name='instance_detail',
    ),
    path(
        'series/<int:pk>/',
        views.SeriesDetailView.as_view(),
        name='series_plot',
    ),
]

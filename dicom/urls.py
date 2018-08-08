from django.urls import path

from . import views

urlpatterns = [
    path(
        'new/',
        views.InstancesCreateView.as_view(),
        name='instances_create',
    ),
    path(
        'instances/',
        views.InstanceListView.as_view(),
        name='instance_list',
    ),
    path(
        '<int:pk>/',
        views.InstanceDetailView.as_view(),
        name='instance_detail',
    ),
    path(
        'series/',
        views.SeriesListView.as_view(),
        name='series_list',
    ),
    path(
        'series/<int:pk>/',
        views.SeriesDetailView.as_view(),
        name='series_detail',
    ),
    path(
        'studies/',
        views.StudyListView.as_view(),
        name='dicom_study_list',
    ),
    path(
        'study/<int:pk>/',
        views.StudyDetailView.as_view(),
        name='dicom_study_detail',
    ),
    path(
        'patients/',
        views.PatientListView.as_view(),
        name='patient_list',
    ),
    path(
        'patients/<int:pk>/',
        views.PatientDetailView.as_view(),
        name='patient_detail',
    ),
]

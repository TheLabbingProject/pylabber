from django.urls import path

from . import views

urlpatterns = [
    path(
        'studies/',
        views.StudyListView.as_view(),
        name='studies',
    ),
    path(
        'studies/new/',
        views.StudyCreateView.as_view(),
        name='study_new',
    ),
    path(
        'studies/<int:pk>/delete/',
        views.StudyDeleteView.as_view(),
        name='study_delete'),
    path(
        'studies/<int:pk>/edit/',
        views.StudyUpdateView.as_view(),
        name='study_edit'),
    path(
        'studies/<int:pk>/',
        views.StudyDetailView.as_view(),
        name='study_detail'),
]

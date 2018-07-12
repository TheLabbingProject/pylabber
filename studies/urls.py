from django.urls import path

from . import views

urlpatterns = [
    path('', views.StudyListView.as_view(), name='studies'),
    path('new/', views.StudyCreateView.as_view(), name='study_new'),
    path(
        '<int:pk>/delete/',
        views.StudyDeleteView.as_view(),
        name='study_delete'),
    path('<int:pk>/edit/', views.StudyUpdateView.as_view(), name='study_edit'),
    path('<int:pk>/', views.StudyDetailView.as_view(), name='study_detail'),
]

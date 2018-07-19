from django.urls import path

from . import views

urlpatterns = [
    path(
        '<int:pk>/',
        views.UserDetailView.as_view(),
        name='user_detail',
    ),
    path(
        '<int:pk>/edit',
        views.ProfileUpdateView.as_view(),
        name='profile_update',
    ),
]

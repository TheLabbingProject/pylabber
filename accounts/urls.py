from django.urls import path, include
from accounts import views
from rest_framework import routers


app_name = "accounts"
router = routers.DefaultRouter()
router.register(r"group", views.GroupViewSet, basename="group")
router.register(r"laboratory", views.LaboratoryViewSet, basename="laboratory")
router.register(r"profile", views.ProfileViewSet, basename="profile")
router.register(r"user", views.UserViewSet, basename="user")


urlpatterns = [path("accounts/", include(router.urls))]

from django.urls import path, include
from accounts import views
from rest_framework import routers


app_name = "accounts"
router = routers.DefaultRouter()
router.register(r"group", views.GroupViewSet, base_name="group")
router.register(r"laboratory", views.LaboratoryViewSet, base_name="laboratory")
router.register(r"profile", views.ProfileViewSet, base_name="profile")
router.register(r"user", views.UserViewSet, base_name="user")


urlpatterns = [path("accounts/", include(router.urls))]

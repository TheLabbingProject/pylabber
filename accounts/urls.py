from django.urls import path, include
from accounts import views
from rest_framework import routers


app_name = "accounts"
router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profiles", views.ProfileViewSet)
router.register(r"groups", views.GroupViewSet)


urlpatterns = [
    path("accounts/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

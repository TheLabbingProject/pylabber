from django.urls import path, include
from accounts import views
from rest_framework import routers


app_name = "accounts"
router = routers.DefaultRouter()

router.register(r"group", views.GroupViewSet)
router.register(r"laboratory", views.LaboratoryViewSet)
router.register(r"profile", views.ProfileViewSet)
router.register(r"user", views.UserViewSet)


urlpatterns = [path("accounts/", include(router.urls))]

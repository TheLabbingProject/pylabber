from django.urls import include, path
from rest_framework import routers

from accounts import views

app_name = "accounts"
router = routers.DefaultRouter()

router.register(r"group", views.GroupViewSet)
router.register(r"laboratory", views.LaboratoryViewSet)
router.register(r"profile", views.ProfileViewSet)
router.register(r"user", views.UserViewSet)
router.register(r"export_destination", views.ExportDestinationViewSet)
router.register(r"task_result", views.TaskResultViewSet)


urlpatterns = [
    path("accounts/", include(router.urls)),
    path(
        "accounts/institutionList/",
        views.UserViewSet.as_view({"get": "get_institutions"}),
        name="get_institutions",
    ),
    path(
        "accounts/export_destination/export_instance/",
        views.ExportDestinationViewSet.as_view({"POST": "export_instance"}),
        name="export_instance",
    ),
    path(
        "accounts/export_destination/<int:pk>/status/",
        views.ExportDestinationViewSet.as_view({"get": "get_status"}),
        name="export_instance_status",
    ),
]

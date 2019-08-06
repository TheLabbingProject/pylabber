from django.urls import include, path
from research import views
from rest_framework import routers

app_name = "research"
router = routers.DefaultRouter()
router.register(r"studies", views.StudyViewSet)
router.register(r"subjects", views.SubjectViewSet)
router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("research/", include(router.urls)),
    path(
        "research/subject_from_patient/<int:patient_id>/",
        views.SubjectViewSet.as_view({"get": "by_dicom_patient"}),
    ),
]

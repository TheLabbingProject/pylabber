from django.urls import include, path
from research import views
from rest_framework import routers

app_name = "research"
router = routers.DefaultRouter()
router.register(r"studies", views.StudyViewSet)
router.register(r"subjects", views.SubjectViewSet)

urlpatterns = [
    path("research/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

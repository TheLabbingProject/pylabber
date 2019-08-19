from django.urls import include, path
from research import views
from rest_framework import routers

app_name = "research"
router = routers.DefaultRouter()
router.register(r"study", views.StudyViewSet)
router.register(r"subject", views.SubjectViewSet)
router.register(r"group", views.GroupViewSet)

urlpatterns = [path("research/", include(router.urls))]


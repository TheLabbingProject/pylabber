from django.urls import include, path
from rest_framework import routers

from research import views

app_name = "research"
router = routers.DefaultRouter()
router.register(r"study", views.StudyViewSet)
router.register(r"subject", views.SubjectViewSet)
router.register(r"group", views.GroupViewSet)
router.register(r"procedure", views.ProcedureViewSet)
router.register(r"event", views.EventViewSet)
router.register(
    r"procedure_step", views.ProcedureStepViewSet, basename="procedure_step"
)
router.register(r"task", views.TaskViewSet)
router.register(
    r"measurement", views.MeasurementDefinitionViewSet, basename="measurement"
)
router.register(r"data_acquisition", views.DataAcquisitionViewSet)

urlpatterns = [
    path(
        "research/procedure/items/",
        views.ProcedureViewSet.as_view({"get": "get_items"}),
        name="get_procedure_items",
    ),
    path(
        "research/event/items/",
        views.EventViewSet.as_view({"get": "get_items"}),
        name="get_event_items",
    ),
    path(
        "research/measurement/items/",
        views.MeasurementDefinitionViewSet.as_view({"get": "get_items"}),
        name="get_measurement_definition_items",
    ),
    path(
        "research/subject/export/",
        views.SubjectViewSet.as_view({"post": "export_files"}),
        name="export_subject_data",
    ),
    path(
        "research/study/aggregate/",
        views.StudyViewSet.as_view({"get": "aggregate"}),
        name="study_aggregations",
    ),
    path("research/", include(router.urls)),
]

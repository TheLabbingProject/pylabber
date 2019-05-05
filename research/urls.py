from django.urls import path
from research import views

app_name = "research"

urlpatterns = [
    path("studies/", views.StudyListView.as_view(), name="study_list"),
    path("studies/new/", views.StudyCreateView.as_view(), name="study_create"),
    path("studies/<int:pk>/", views.StudyDetailView.as_view(), name="study_detail"),
    path(
        "studies/<int:study_id>/subject/<int:subject_id>/",
        views.embeddable_subject_view,
        name="study_subject_detail",
    ),
    path(
        "embed/subject/<int:subject_id>/",
        views.embeddable_subject_view,
        name="embed_subject_detail",
    ),
    path(
        "studies/<int:pk>/edit/", views.StudyUpdateView.as_view(), name="study_update"
    ),
    path(
        "studies/<int:pk>/delete/", views.StudyDeleteView.as_view(), name="study_delete"
    ),
    path("studies/dicom/json/", views.generate_study_mri_json, name="study_dicom_json"),
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/new/", views.SubjectCreateView.as_view(), name="subject_create"),
    path(
        "subjects/<int:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"
    ),
    path(
        "subjects/<int:pk>/edit/",
        views.SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "subjects/<int:pk>/delete/",
        views.SubjectDeleteView.as_view(),
        name="subject_delete",
    ),
    # path("data/", views.DataSummaryView.as_view(), name="data_summary"),
    # path("data_sources/", views.RemoteLocationListView.as_view(), name="data_sources"),
    # path("import/", views.import_node, name="import_data"),
]

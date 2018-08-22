from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:pk>/',
        views.QuestionnaireDetailView.as_view(),
        name='questionnaire_detail',
    ),
    path(
        'new/',
        views.QuestionnaireCreateView.as_view(),
        name='questionnaire_create',
    ),
]

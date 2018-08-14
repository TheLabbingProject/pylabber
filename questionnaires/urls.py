from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:pk>/',
        views.QuestionnaireDetailView.as_view(),
        name='questionnaire_detail',
    ),
]

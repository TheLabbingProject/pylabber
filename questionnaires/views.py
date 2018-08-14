from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Questionnaire


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_detail.html'

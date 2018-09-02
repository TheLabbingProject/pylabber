from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .models import Questionnaire


class QuestionnaireCreateView(LoginRequiredMixin, CreateView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_create.html'
    fields = [
        'name',
        'description',
    ]


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_detail.html'

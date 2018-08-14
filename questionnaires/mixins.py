from .models import Questionnaire


class QuestionnaireListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.all()
        return context

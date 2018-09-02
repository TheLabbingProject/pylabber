from .models import Questionnaire


def questionnaires(request):
    return {'questionnaires': Questionnaire.objects.all()}
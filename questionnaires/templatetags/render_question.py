from django import template
from django.template.loader import get_template

register = template.Library()

template_dict = {
    'RatingQuestion':
    'questionnaires/questions/rating_question.html',
    'OpenQuestion':
    'questionnaires/questions/open_question.html',
    'MultipleChoiceQuestion':
    'questionnaires/questions/multiple_choice_question.html',
}


def render_open_question(question):
    return {
        'text': question.text,
    }


def render_multiple_choice_question(question):
    return {
        'text': question.text,
        'options': question.multiplechoicequestion.options.all()
    }


@register.inclusion_tag(template_dict['RatingQuestion'])
def render_rating_question(question):
    return {
        'text': question.text,
        'range': question.ratingquestion.get_range()
    }
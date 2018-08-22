from django import template

register = template.Library()

template_dict = {
    'RatingQuestion':
    'questionnaires/questions/rating_question.html',
    'OpenQuestion':
    'questionnaires/questions/open_question.html',
    'MultipleChoiceQuestion':
    'questionnaires/questions/multiple_choice_question.html',
}


@register.inclusion_tag(template_dict['OpenQuestion'])
def render_open_question(question):
    return {
        'text': question.text,
    }


@register.inclusion_tag(template_dict['MultipleChoiceQuestion'])
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
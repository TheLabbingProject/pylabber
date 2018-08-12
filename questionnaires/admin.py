from django.contrib import admin
from .models import (
    Questionnaire,
    OpenQuestion,
    MultipleChoiceQuestion,
    Option,
    RatingQuestion,
    ShortOpenAnswer,
    LongOpenAnswer,
    MultipleChoiceAnswer,
    RatingAnswer,
)


class QuestionInLine(admin.StackedInline):
    model = Questionnaire.questions.through
    verbose_name = 'Question'
    verbose_name_plural = 'Questions'
    extra = 1


class QuestionnairesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    inlines = (QuestionInLine, )
    exclude = ('questions', )


# class QuestionsAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'text',
#         'solution',
#     )

# class AnswersAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'questionnaire',
#         'subject',
#         'question',
#         'choice',
#         '_is_correct',
#     )
#     ordering = ['questionnaire', 'subject', 'question']

admin.site.register(Questionnaire, QuestionnairesAdmin)
admin.site.register(OpenQuestion)
admin.site.register(ShortOpenAnswer)
admin.site.register(LongOpenAnswer)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(Option)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(RatingQuestion)
admin.site.register(RatingAnswer)
# admin.site.register(Question, QuestionsAdmin)
# admin.site.register(Option)
# admin.site.register(Answer, AnswersAdmin)

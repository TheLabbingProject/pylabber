from django.contrib import admin
from .models import Questionnaire, Question, Option, Answer


class QuestionInLine(admin.StackedInline):
    model = Questionnaire.questions.through
    verbose_name = 'Question'
    verbose_name_plural = 'Questions'
    extra = 1
    readonly_fields = (
        'options',
        'solution',
    )

    def options(self, instance):
        return [str(option) for option in instance.question.options.all()]

    def solution(self, instance):
        return instance.question.solution


class QuestionnairesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    inlines = (QuestionInLine, )


class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'solution',
    )


class AnswersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'questionnaire',
        'subject',
        'question',
        'choice',
        '_is_correct',
    )
    ordering = ['questionnaire', 'subject', 'question']


admin.site.register(Questionnaire, QuestionnairesAdmin)
admin.site.register(Question, QuestionsAdmin)
admin.site.register(Option)
admin.site.register(Answer, AnswersAdmin)

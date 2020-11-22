from django.contrib import admin
from research.models.event import Event
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep
from research.models.study import Study
from research.models.subject import Subject
from research.models.task import Task


class SubjectsInline(admin.TabularInline):
    model = Study.subjects.through
    verbose_name_plural = "Subjects"
    extra = 0
    readonly_fields = (
        "id_number",
        "first_name",
        "last_name",
        "sex",
        "date_of_birth",
    )

    def id_number(self, instance):
        return instance.subject.id_number

    def first_name(self, instance):
        return instance.subject.first_name

    def last_name(self, instance):
        return instance.subject.last_name

    def sex(self, instance):
        return instance.subject.sex

    def date_of_birth(self, instance):
        return instance.subject.date_of_birth


class CollaboratorsInline(admin.TabularInline):
    model = Study.collaborators.through
    verbose_name_plural = "Collaborators"
    extra = 0


class StudiesAdmin(admin.ModelAdmin):
    inlines = CollaboratorsInline, SubjectsInline
    list_display = "title", "description", "created"
    exclude = "subjects", "collaborators"


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "id_number",
        "first_name",
        "last_name",
        "sex",
        "date_of_birth",
        "dominant_hand",
    )
    list_filter = ("sex",)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context
        )
        return response


class ProcedureStepInline(admin.TabularInline):
    model = ProcedureStep
    extra = 0
    fields = (
        "index",
        "event_type",
        "event_title",
        "event_description",
    )
    readonly_fields = (
        "index",
        "event_type",
        "event_title",
        "event_description",
    )

    def event_type(self, instance) -> str:
        event = Event.objects.select_subclasses().get(id=instance.id)
        event_type = event.__class__.__name__
        return (
            event_type
            if event_type != "MeasurementDefinition"
            else "Measurement"
        )

    def event_title(self, instance) -> str:
        return instance.event.title

    def event_description(self, instance) -> str:
        return instance.event.description


class StudyInline(admin.TabularInline):
    model = Study.procedures.through
    verbose_name_plural = "Studies"
    extra = 0


class ProcedureAdmin(admin.ModelAdmin):
    list_display = "id", "title", "description"
    inlines = ProcedureStepInline, StudyInline


class MeasurementDefinitionAdmin(admin.ModelAdmin):
    list_display = "id", "title", "description"


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
    )


admin.site.register(MeasurementDefinition, MeasurementDefinitionAdmin)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Study, StudiesAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)

from django.contrib import admin
from research.models.study import Study
from research.models.subject import Subject


class SubjectsInline(admin.TabularInline):
    model = Study.subjects.through
    verbose_name_plural = "Subjects"
    readonly_fields = ("id_number", "first_name", "last_name", "sex", "date_of_birth")

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


class StudiesAdmin(admin.ModelAdmin):
    inlines = (SubjectsInline, CollaboratorsInline)
    list_display = ("title", "description", "created")
    exclude = ("subjects", "collaborators")


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
        response = super().changelist_view(request, extra_context=extra_context)
        return response


admin.site.register(Study, StudiesAdmin)
admin.site.register(Subject, SubjectAdmin)

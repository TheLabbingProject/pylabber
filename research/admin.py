from django.contrib import admin

# from django.conf import settings
from .models import Study, Subject

# if 'dicomdj' in settings.INSTALLED_APPS:
#     from dicomdj.admin import PatientInLine


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
        "id_number",
        "first_name",
        "last_name",
        "sex",
        "date_of_birth",
        "dominant_hand",
    )
    # inlines = (PatientInLine, )


admin.site.register(Study, StudiesAdmin)
admin.site.register(Subject, SubjectAdmin)

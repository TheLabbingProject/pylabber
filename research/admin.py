from django.contrib import admin

from .models import Study, Subject


class SubjectsInline(admin.TabularInline):
    model = Study.subjects.through
    verbose_name_plural = 'Subjects'
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
    )

    def first_name(self, instance):
        return self.instance.first_name

    def last_name(self, instance):
        return self.instance.last_name

    def email(self, instance):
        return self.instance.email


class CollaboratorsInline(admin.TabularInline):
    model = Study.collaborators.through
    verbose_name_plural = 'Collaborators'


class StudiesAdmin(admin.ModelAdmin):
    inlines = (
        SubjectsInline,
        CollaboratorsInline,
    )
    list_display = (
        'name',
        'description',
        'created_at',
    )
    exclude = ('subjects', 'collaborators')


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'sex',
        'date_of_birth',
        'email',
        'phone_number',
    )


admin.site.register(Study, StudiesAdmin)
admin.site.register(Subject, SubjectAdmin)

from django.contrib import admin
from .models import Instance, Series, Study, Patient


class InstanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'instance_uid',
        'patient',
        'series',
        'number',
        'date',
        'time',
    )
    ordering = ['-date', '-series', 'number']
    readonly_fields = ['instance_uid']


class InstanceInLine(admin.TabularInline):
    model = Instance
    exclude = (
        'instance_uid',
        'date',
        'time',
    )
    ordering = ['date', 'time']


class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'series_uid',
        'date',
        'time',
        'number',
        'description',
    )
    ordering = ['-date', '-time']
    inlines = (InstanceInLine, )
    readonly_fields = ['series_uid']


class StudyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'study_uid',
        'description',
    )
    inlines = (InstanceInLine, )
    readonly_fields = ['study_uid']


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient_uid',
        'given_name',
        'family_name',
        'sex',
        'date_of_birth',
    )
    inlines = (InstanceInLine, )
    fieldsets = (
        (None, {
            'fields': ('patient_uid', ),
        }),
        ('Name', {
            'fields': (
                'name_prefix',
                'given_name',
                'middle_name',
                'family_name',
                'name_suffix',
            ),
        }),
        ('Personal Information', {
            'fields': (
                'sex',
                'date_of_birth',
            )
        }),
        ('Associated Model', {
            'fields': ('subject', )
        }),
    )


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Patient, PatientAdmin)

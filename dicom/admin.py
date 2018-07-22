from django.contrib import admin
from .models import Instance, Series, Study, Patient


class InstanceInLine(admin.TabularInline):
    model = Instance
    exclude = (
        'date',
        'time',
    )
    ordering = ('date', 'time')


class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'time',
        'number',
        'description',
    )
    ordering = ['-date', '-time']
    inlines = (InstanceInLine, )


class StudyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'description',
    )
    inlines = (InstanceInLine, )


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'given_name',
        'family_name',
        'sex',
        'date_of_birth',
    )
    inlines = (InstanceInLine, )
    fieldsets = (
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


admin.site.register(Instance)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Patient, PatientAdmin)

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


class PatientInLine(admin.StackedInline):
    model = Patient
    verbose_name_plural = 'MRI'
    fields = (
        'studies',
        'series_count',
        'dicom_count',
    )
    readonly_fields = (
        'studies',
        'series_count',
        'dicom_count',
    )

    def get_series(self, instance):
        return Series.objects.filter(patient=instance)

    def series_count(self, instance):
        return self.get_series(instance).count()

    def get_studies(self, instance):
        return Study.objects.filter(
            id__in=self.get_series(instance).values('study').distinct())

    def get_study_list(self, instance):
        return self.get_studies(instance).values_list('description')

    def studies(self, instance):
        return [study for study in self.get_study_list(instance)]

    def dicom_count(self, instance):
        return Instance.objects.filter(patient=instance).count()

    dicom_count.short_description = 'DICOM files'


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

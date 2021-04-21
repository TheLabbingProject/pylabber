from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_mri.models.session import Session

from research.models.event import Event
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep
from research.models.study import Study
from research.models.subject import Subject
from research.models.task import Task
from research.utils.html import Html

DOWNLOAD_BUTTON = '<span style="padding-left:20px;"><a href={url} type="button" class="button" id="{file_format}-download-button">{text}</a></span>'  # noqa: E501


class SessionInLine(admin.TabularInline):
    model = Session
    verbose_name_plural = "MRI Sessions"
    fields = (
        "id_link",
        "time",
        "measurement",
        "scan_count",
        "comments",
        "download",
    )
    readonly_fields = "id_link", "time", "scan_count", "download"
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: Session):
        return False

    def id_link(self, instance: Session) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    def scan_count(self, instance: Session) -> int:
        return instance.scan_set.count()

    def download(self, instance: Session) -> str:
        links = ""
        url = reverse("mri:session_nifti_zip", args=(instance.id,))
        button = DOWNLOAD_BUTTON.format(
            url=url, file_format="nifti", text="NIfTI"
        )
        links += button
        first_scan = instance.scan_set.first()
        if first_scan.dicom:
            url = reverse("mri:session_dicom_zip", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, file_format="dicom", text="DICOM"
            )
            links += button
        return mark_safe(links)

    id_link.short_description = "ID"


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
    fields = "user_id", "title", "first_name", "last_name", "username", "email"
    readonly_fields = (
        "user_id",
        "title",
        "first_name",
        "last_name",
        "username",
        "email",
    )
    can_delete = False

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: Session):
        return False

    def user_id(self, instance) -> str:
        model_name = instance.user.__class__.__name__
        pk = instance.user.id
        return Html.admin_link(model_name, pk)

    user_id.short_description = "ID"

    def title(self, instance) -> str:
        return instance.user.profile.get_title_repr()

    def first_name(self, instance) -> str:
        return instance.user.first_name

    def last_name(self, instance) -> str:
        return instance.user.last_name

    def username(self, instance) -> str:
        return instance.user.username

    def email(self, instance) -> str:
        return instance.user.email


class ProcedureInline(admin.TabularInline):
    model = Study.procedures.through
    extra = 0
    can_delete = False
    verbose_name_plural = "Procedures"
    fields = (
        "id_link",
        "title",
        "description",
    )
    readonly_fields = (
        "id_link",
        "title",
        "description",
    )

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance):
        return False

    def id_link(self, instance) -> str:
        procedure = instance.procedure
        model_name = procedure.__class__.__name__
        return Html.admin_link(model_name, procedure.id)

    def title(self, instance) -> str:
        return instance.procedure.title

    def description(self, instance) -> str:
        return instance.procedure.description

    id_link.short_description = "ID"


class StudyAdmin(admin.ModelAdmin):
    inlines = CollaboratorsInline, ProcedureInline, SubjectsInline
    list_display = "title", "description", "created"
    exclude = "subjects", "collaborators", "procedures"


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "id_number",
        "first_name",
        "last_name",
        "sex",
        "date_of_birth",
        "dominant_hand",
        "n_mri_sessions",
    )
    search_fields = "id", "id_number", "first_name", "last_name"
    list_filter = "sex", "dominant_hand"
    readonly_fields = ("n_mri_sessions",)
    inlines = (SessionInLine,)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context
        )
        return response

    def n_mri_sessions(self, instance: Subject) -> int:
        return instance.mri_session_set.count()

    n_mri_sessions.short_description = "# MRI Sessions"


class ProcedureStepInline(admin.TabularInline):
    model = ProcedureStep
    extra = 0
    fields = (
        "index_link",
        "event_type",
        "event_title",
        "event_description",
    )
    readonly_fields = (
        "index_link",
        "event_type",
        "event_title",
        "event_description",
    )
    can_delete = False
    verbose_name_plural = "Steps"

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: ProcedureStep):
        return False

    def index_link(self, instance: ProcedureStep) -> str:
        event = Event.objects.get_subclass(id=instance.event.id)
        model_name = event.__class__.__name__
        pk = instance.event.id
        text = str(instance.index)
        return Html.admin_link(model_name, pk, text)

    def event_title(self, instance: ProcedureStep) -> str:
        return instance.event.title

    def event_type(self, instance: ProcedureStep) -> str:
        event = Event.objects.get_subclass(id=instance.event.id)
        event_type = event.__class__.__name__
        return (
            event_type
            if event_type != "MeasurementDefinition"
            else "Measurement"
        )

    def event_description(self, instance: ProcedureStep) -> str:
        return instance.event.description

    index_link.short_description = "Index"
    event_title.short_description = "Title"
    event_description.short_description = "Description"
    event_type.short_description = "Type"


class StudyInline(admin.TabularInline):
    model = Study.procedures.through
    fields = "id_link", "title", "description"
    readonly_fields = "id_link", "title", "description"
    verbose_name_plural = "Studies"
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: ProcedureStep):
        return False

    def id_link(self, instance) -> str:
        model_name = instance.study.__class__.__name__
        pk = instance.study.id
        return Html.admin_link(model_name, pk)

    def title(self, instance) -> str:
        return instance.study.title

    def description(self, instance) -> str:
        return instance.study.description

    id_link.short_description = "ID"


class ProcedureAdmin(admin.ModelAdmin):
    list_display = "id", "title", "description", "step_count"
    inlines = StudyInline, ProcedureStepInline

    def step_count(self, instance: Procedure) -> int:
        return instance.step_set.count()


class MeasurementDefinitionAdmin(admin.ModelAdmin):
    list_display = "id", "title", "description", "content_type", "n_collected"

    def n_collected(self, instance: MeasurementDefinition) -> int:
        try:
            return instance.instance_set.count()
        except AttributeError:
            pass

    n_collected.short_description = "# Collected"


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
    )


admin.site.register(MeasurementDefinition, MeasurementDefinitionAdmin)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)

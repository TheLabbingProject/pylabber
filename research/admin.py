from datetime import date, datetime

from bokeh.embed import autoload_static
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.resources import CDN
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_admin_inline_paginator.admin import TabularInlinePaginated
from django_mri.admin import create_scan_download_links
from django_mri.models.session import Session

from research.models.event import Event
from research.models.group import Group
from research.models.measurement_definition import MeasurementDefinition
from research.models.procedure import Procedure
from research.models.procedure_step import ProcedureStep
from research.models.study import Study
from research.models.subject import Subject
from research.models.task import Task
from research.utils.html import Html

DOWNLOAD_BUTTON = '<span style="padding-left:20px;"><a href={url} type="button" class="button" id="{file_format}-download-button">{text}</a></span>'  # noqa: E501
LINK_BUTTON = '<a href={url} type="button" class="button">{text}</a>'


def custom_titled_filter(title: str):
    """
    Copied from SO:
    https://stackoverflow.com/a/21223908/4416932
    """

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("decade born")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "decade"

    DECADES = "40s", "50s", "60s", "70s", "80s", "90s", "00s"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((decade, _(decade)) for decade in self.DECADES)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "40s":
            gte = date(1940, 1, 1)
            lte = date(1949, 12, 31)
        elif self.value() == "50s":
            gte = date(1950, 1, 1)
            lte = date(1959, 12, 31)
        elif self.value() == "60s":
            gte = date(1960, 1, 1)
            lte = date(1969, 12, 31)
        elif self.value() == "70s":
            gte = (date(1970, 1, 1),)
            lte = date(1979, 12, 31)
        elif self.value() == "80s":
            gte = date(1980, 1, 1)
            lte = date(1989, 12, 31)
        elif self.value() == "90s":
            gte = date(1990, 1, 1)
            lte = date(1999, 12, 31)
        elif self.value() == "00s":
            gte = date(2000, 1, 1)
            lte = date(2009, 12, 31)
        else:
            return queryset.all()
        return queryset.filter(date_of_birth__gte=gte, date_of_birth__lte=lte)


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

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance):
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
    fields = "title", "description", "image", "participant_list"
    readonly_fields = ("participant_list",)
    inlines = CollaboratorsInline, ProcedureInline
    list_display = "title", "description", "created"
    exclude = "subjects", "collaborators", "procedures"

    def participant_list(self, instance: Study) -> str:
        subjects_view = reverse("admin:research_subject_changelist")
        url = f"{subjects_view}?study+participation={instance.id}"
        html = LINK_BUTTON.format(url=url, text="View")
        return mark_safe(html)

    participant_list.short_description = "Participants"


class ScanInline(TabularInlinePaginated):
    model = Group.mri_scan_set.through
    extra = 0
    verbose_name_plural = "Scans"
    fields = (
        "id_link",
        "subject",
        "session",
        "number",
        "time",
        "description",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution",
        "comments",
        "download",
    )
    readonly_fields = (
        "id_link",
        "subject",
        "session",
        "number",
        "time",
        "description",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution",
        "comments",
        "download",
    )

    class Media:
        css = {"all": ("research/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance):
        return False

    def subject(self, instance) -> str:
        subject = instance.scan.session.subject
        model_name = subject.__class__.__name__
        text = subject.id_number
        return Html.admin_link(model_name, subject.id, text)

    def session(self, instance) -> str:
        session = instance.scan.session
        model_name = session.__class__.__name__
        return Html.admin_link(model_name, session.id)

    def id_link(self, instance) -> str:
        model_name = instance.scan.__class__.__name__
        return Html.admin_link(model_name, instance.scan.id)

    def number(self, instance) -> int:
        return instance.scan.number

    def description(self, instance) -> str:
        return instance.scan.description

    def comments(self, instance) -> str:
        return instance.scan.comments or ""

    def time(self, instance) -> datetime:
        return instance.scan.time.strftime("%Y-%m-%d %H:%M:%S")

    def echo_time(self, instance) -> float:
        return instance.scan.echo_time

    def inversion_time(self, instance) -> float:
        return instance.scan.inversion_time

    def repetition_time(self, instance) -> float:
        return instance.scan.repetition_time

    def spatial_resolution(self, instance) -> str:
        """
        Returns a nicely formatted representation of the scan's spatial
        resolution.

        Parameters
        ----------
        instance : django_mri.Scan_study_groups
            Scan_study_groups instance

        Returns
        -------
        str
            Formatted spatial resolution representation
        """

        try:
            return " x ".join(
                [
                    f"{number:.2g}"
                    for number in instance.scan.spatial_resolution
                ]
            )
        except TypeError:
            return ""

    def download(self, instance) -> str:
        return create_scan_download_links(instance.scan)

    id_link.short_description = "ID"


class GroupAdmin(admin.ModelAdmin):
    inlines = (ScanInline,)
    list_display = "id", "study_", "title", "description", "mri_scan_count"
    readonly_fields = "study_", "mri_scan_count"
    search_fields = "study__title", "title", "description"
    list_filter = (
        "title",
        ("study__title", custom_titled_filter("study title")),
    )

    def mri_scan_count(self, instance: Group) -> int:
        return instance.mri_scan_set.count()

    def study_(self, instance: Group) -> str:
        model_name = instance.study.__class__.__name__
        pk = instance.study.id
        text = instance.study.title
        return Html.admin_link(model_name, pk, text)

    mri_scan_count.short_description = "# MRI Scans"


class StudyAssociationFilter(SimpleListFilter):
    title = "study participation"
    parameter_name = "study participation"

    def lookups(self, request, model_admin):
        return [(study.id, study.title) for study in Study.objects.all()]

    def queryset(self, request, queryset):
        try:
            value = int(self.value())
        except TypeError:
            return queryset
        else:
            subject_ids = [
                subject.id
                for subject in queryset.all()
                if value in subject.query_studies(id_only=True)
            ]
            return queryset.filter(id__in=subject_ids)


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
    search_fields = (
        "id",
        "id_number",
        "first_name",
        "last_name",
        "date_of_birth__year",
    )
    list_filter = (
        "sex",
        "dominant_hand",
        DecadeBornListFilter,
        StudyAssociationFilter,
    )
    readonly_fields = ("n_mri_sessions",)
    inlines = (SessionInLine,)
    actions = ("export_csv",)

    @admin.action(description="Export CSV")
    def export_csv(self, request, queryset):
        df = queryset.to_dataframe()
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=subjects.csv"
            },
        )
        df.to_csv(path_or_buf=response)
        return response

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context
        )
        if hasattr(response, "context_data"):
            queryset = response.context_data["cl"].queryset
            if queryset.exists():
                # output_file("bokeh_tmp.html")

                sex_plot = queryset.plot_bokeh_sex_pie()
                dominant_hand_plot = queryset.plot_bokeh_dominant_hand_pie()
                dob_plot = queryset.plot_bokeh_date_of_birth()
                figure_layout = [[sex_plot, dominant_hand_plot]]
                if dob_plot is not None:
                    figure_layout[0].append(dob_plot)
                figure = layout(figure_layout)
                js, tag = autoload_static(figure, CDN, "tmp_bokeh_figure")
                curdoc().theme = "dark_minimal"
                extra_context = {"bokeh_tag": tag, "bokeh_js": js}
                response.context_data.update(extra_context)
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


admin.site.register(Group, GroupAdmin)
admin.site.register(MeasurementDefinition, MeasurementDefinitionAdmin)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)

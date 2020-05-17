from bokeh.layouts import column
from bokeh.models import Div, Select
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from plots.model_explorer.templates.field_info_table import FIELD_INFO_TABLE
from titlecase import titlecase


class FieldSelector:
    EXCLUDED_APPS = (
        "accounts",
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "authtoken",
    )
    EXCLUDED_FIELD_TYPES = (
        models.AutoField,
        models.ForeignKey,
        models.ManyToManyField,
        models.ManyToOneRel,
        models.ManyToManyRel,
    )

    def __init__(self, raw_models: list):
        self.raw_models = raw_models
        self.models = self.get_models_dict(self.raw_models)
        self.app_select = self.create_app_select()
        self.model_select = self.create_model_select()
        self.field_select = self.create_field_select()
        self.field_info = Div(text="")
        self.update_field_info()

    @staticmethod
    def fix_field_name(field_name: str) -> str:
        return titlecase(field_name.replace("_", " "))

    @classmethod
    def get_models_dict(cls, raw_models: list) -> dict:
        result = {}
        for model in raw_models:
            app_label, model_name = model._meta.label.split(".")
            if app_label not in cls.EXCLUDED_APPS:
                if app_label not in result:
                    result[app_label] = {}
                result[app_label][model_name] = model
        return result

    def create_app_select(self) -> Select:
        options = list(self.models.keys())
        value = options[0]
        app_select = Select(title="App", options=options, value=value)
        app_select.on_change("value", self.handle_app_selection)
        return app_select

    def handle_app_selection(self, attr: str, old: str, new: str):
        if new:
            self.model_select.options = list(self.models[new].keys())
            self.model_select.value = self.model_select.options[0]
            self.model_select.disabled = False
        else:
            self.model_select.options = []
            self.model_select.disabled = True

    def create_model_select(self) -> Select:
        app_label = self.app_select.value
        if app_label:
            options = list(self.models[app_label].keys())
            disabled = False
            value = options[0]
        else:
            options = []
            disabled = True
            value = None
        model_select = Select(
            title="Model", options=options, value=value, disabled=disabled
        )
        model_select.on_change("value", self.handle_model_selection)
        return model_select

    def handle_model_selection(self, attr: str, old: str, new: str):
        self.field_select.options = self.create_field_options()
        self.update_field_info()

    def create_field_options(self):
        if self.selected_model:
            return [
                (field.name, self.fix_field_name(field.name))
                for field in self.selected_model._meta.get_fields()
                if not isinstance(field, self.EXCLUDED_FIELD_TYPES)
            ]

    def create_field_select(self) -> Select:
        options = self.create_field_options()
        value = options[0][0] if options else None
        field_select = Select(title="Field", options=options, value=value)
        field_select.on_change("value", self.handle_field_selection)
        return field_select

    def handle_field_selection(self, attr: str, old: str, new: str) -> None:
        self.update_field_info()

    def update_field_info(self) -> Div:
        if self.selected_field:
            field_type = self.selected_field.__class__.__name__
            description = self.selected_field.description
            help_text = self.selected_field.help_text
            text = FIELD_INFO_TABLE.format(
                field_label=str(self.selected_field),
                field_type=field_type,
                description=description,
                help_text=help_text,
            )
            self.field_info.text = text
        else:
            self.field_info.text = ""

    def create_layout(self):
        hr = Div(text="<hr />", style={"width": "100%"})
        return column(
            self.app_select, self.model_select, self.field_select, hr, self.field_info
        )

    @property
    def selected_model(self) -> models.Model:
        app_label = self.app_select.value
        model_name = self.model_select.value
        if app_label and model_name:
            try:
                return self.models[app_label][model_name]
            except LookupError:
                pass

    @property
    def selected_field(self) -> models.Field:
        field_name = self.field_select.value
        if self.selected_model:
            try:
                return self.selected_model._meta.get_field(field_name)
            except FieldDoesNotExist:
                pass

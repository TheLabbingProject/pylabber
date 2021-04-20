import json

from django.urls import reverse
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

ADMIN_VIEW_NAMES = {
    "Subject": "admin:research_subject_change",
    "Study": "admin:research_study_change",
    "Procedure": "admin:research_procedure_change",
    "MeasurementDefinition": "admin:research_measurementdefinition_change",
    "Task": "admin:research_task_change",
    "User": "admin:accounts_user_change",
    "Session": "admin:django_mri_session_change",
}


class Html:
    BREAK = "<br>"
    HORIZONTAL_LINE = '<hr style="background-color: {color};">'

    @classmethod
    def admin_link(cls, model_name: str, pk: int, text: str = None) -> str:
        view_name = ADMIN_VIEW_NAMES.get(model_name)
        if view_name:
            url = reverse(view_name, args=(pk,))
            text = text if isinstance(text, str) else pk
            html = f'<a href="{url}">{text}</a>'
            return mark_safe(html)

    @classmethod
    def break_html(cls, pieces) -> str:
        return mark_safe(cls.BREAK.join(pieces))

    @classmethod
    def horizontal_line(cls, color: str = "black") -> str:
        return cls.HORIZONTAL_LINE.format(color=color)

    @classmethod
    def json(cls, value) -> json:
        response = json.dumps(value, sort_keys=True, indent=4, default=str)
        formatter = HtmlFormatter(style="colorful")
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style>"
        return mark_safe(style + response)

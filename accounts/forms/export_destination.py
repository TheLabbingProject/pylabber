from accounts.models import help_text
from accounts.models.export_destination import ExportDestination
from django.forms import CharField, ModelForm, PasswordInput


class ExportDestinationForm(ModelForm):
    password = CharField(
        widget=PasswordInput(render_value=True),
        help_text=help_text.EXPORT_DESTINATION_PASSWORD,
    )

    class Meta:
        model = ExportDestination
        fields = (
            "id",
            "title",
            "description",
            "ip",
            "port",
            "username",
            "password",
            "destination",
            "socket_timeout",
            "negotiation_timeout",
            "banner_timeout",
            "users",
        )

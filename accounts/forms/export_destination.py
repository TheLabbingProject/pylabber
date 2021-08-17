from accounts.models.export_destination import ExportDestination
from django.forms import CharField, ModelForm, PasswordInput


class ExportDestinationForm(ModelForm):
    password = CharField(widget=PasswordInput())

    class Meta:
        model = ExportDestination
        fields = (
            "title",
            "description",
            "ip",
            "username",
            "password",
            "destination",
            "users",
        )

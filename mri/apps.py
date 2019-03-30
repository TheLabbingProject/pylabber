from django.apps import AppConfig


class MriConfig(AppConfig):
    name = "mri"

    def ready(self):
        import mri.signals

from django.apps import AppConfig


class ResearchConfig(AppConfig):
    name = 'research'

    def ready(self):
        import research.signals
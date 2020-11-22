from django.apps import AppConfig


class ResearchConfig(AppConfig):
    name = "research"

    def ready(self):
        """
        Loads the app's signals.

        References
        ----------
        * :meth:`~django.apps.AppConfig.ready`
        """

        import research.signals  # noqa: F401

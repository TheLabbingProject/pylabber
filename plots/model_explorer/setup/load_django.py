import django
import os

from .configuration import PROJECT_NAME
from .no_stdout import no_stdout
from .project_base import add_project_base_to_path


def prepare_environment() -> None:
    # Settings module location.
    # See:
    # https://docs.djangoproject.com/en/3.0/topics/settings/#envvar-DJANGO_SETTINGS_MODULE
    os.environ["DJANGO_SETTINGS_MODULE"] = f"{PROJECT_NAME}.settings"

    # This settings is required to prevent an async call error from django (==3.0.6).
    # See: https://stackoverflow.com/a/59774008/4416932
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def load_django() -> None:
    add_project_base_to_path()
    prepare_environment()
    with no_stdout():
        django.setup()

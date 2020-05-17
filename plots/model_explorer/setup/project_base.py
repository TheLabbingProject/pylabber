import os
import sys

from pathlib import Path
from .configuration import BASE_PATH_ENV, PROJECT_NAME
from .messages import MISSING_PROJECT_DIR


def search_project_base() -> Path:
    HERE = Path(__file__)
    for i in range(6):
        if HERE.parent.name == PROJECT_NAME:
            return HERE.parent
        HERE = HERE.parent


def get_project_base() -> Path:
    try:
        return Path(os.environ[BASE_PATH_ENV])
    except KeyError:
        return search_project_base()


def add_project_base_to_path() -> None:
    project_base = get_project_base()
    if project_base:
        path = str(project_base.absolute())
        sys.path.insert(0, path)
    else:
        raise RuntimeError(MISSING_PROJECT_DIR)

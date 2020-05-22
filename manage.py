#!/usr/bin/env python
import os
import sys

# from pylabber.plotting.bokeh.server import start_bokeh_server


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pylabber.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # if sys.argv[1] == "runserver":
    #     bokeh_server_process = start_bokeh_server()
    execute_from_command_line(sys.argv)

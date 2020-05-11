import socket
import subprocess

from django.conf import settings

DEFAULT_SETTINGS = {"port": 5006}


def get_bokeh_settings() -> int:
    bokeh_settings = getattr(settings, "BOKEH", DEFAULT_SETTINGS)
    return {**DEFAULT_SETTINGS, **bokeh_settings}


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def get_server_status() -> bool:
    bokeh_settings = get_bokeh_settings()
    port = bokeh_settings["port"]
    return is_port_in_use(port)


def start_bokeh_server() -> subprocess.Popen:
    status = get_server_status()
    if status is False:
        return subprocess.Popen(
            [
                "bokeh",
                "serve",
                "research/plotting/subject/date_of_birth/bokeh",
                "--allow-websocket-origin",
                "localhost:5006",
                "--allow-websocket-origin",
                "127.0.0.1:8000",
            ]
        )

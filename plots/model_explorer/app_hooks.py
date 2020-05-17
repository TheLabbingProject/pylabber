from .setup import load_django


def on_server_loaded(server_context):
    load_django()

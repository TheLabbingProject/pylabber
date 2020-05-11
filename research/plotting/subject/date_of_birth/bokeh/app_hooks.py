import django
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))


def on_server_loaded(server_context):
    os.environ["DJANGO_SETTINGS_MODULE"] = "pylabber.settings"
    django.setup()

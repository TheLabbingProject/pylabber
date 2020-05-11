from django.apps import apps
from django.conf import settings


def get_subject_model():
    app_label, model_name = settings.SUBJECT_MODEL.split(".")
    return apps.get_model(app_label=app_label, model_name=model_name)

from typing import Set

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.db.models.query import QuerySet
from research.utils.messages import INVALID_CONTENT_TYPE

DATA_ACQUISITION_MODELS = getattr(settings, "DATA_ACQUISITION_MODELS", set())


def get_data_acquisition_models() -> QuerySet:
    ids = []
    for content_type in DATA_ACQUISITION_MODELS:
        try:
            model = ContentType.objects.get(**content_type)
        except ContentType.DoesNotExist:
            raise ContentType.DoesNotExist(INVALID_CONTENT_TYPE)
        else:
            ids.append(model.id)
    return ContentType.objects.filter(id__in=ids)

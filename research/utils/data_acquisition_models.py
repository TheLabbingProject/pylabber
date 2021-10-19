"""
Utility functions related to data acquisition models management.
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet, Q

DATA_ACQUISITION_MODELS = getattr(settings, "DATA_ACQUISITION_MODELS", set())


def get_data_acquisition_models() -> QuerySet:
    """
    Returns the registered data acquisition models' content types.

    Returns
    -------
    QuerySet
        Registered data acquisition models
    """
    query = Q()
    for content_type in DATA_ACQUISITION_MODELS:
        query |= Q(**content_type)
    return ContentType.objects.filter(query)

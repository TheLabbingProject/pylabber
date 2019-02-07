from __future__ import absolute_import, unicode_literals

# import celery
from .celery import app as celery_app


__all__ = ("celery_app",)

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False


class MediaStorage(S3Boto3Storage):
    location = getattr(settings, "PUBLIC_MEDIA_LOCATION", "media")
    file_overwrite = False
    default_acl = "public-read"

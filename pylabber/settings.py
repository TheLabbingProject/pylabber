"""
Django settings for pylabber project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from pathlib import Path

# import django_heroku
import environ
from django_mri.analysis.mri_interfaces import interfaces

# from django_mri.analysis.visualizers import MRI_VISUALIZERS

###############
# Environment #
###############

# Environment variables are expected to be set in a .env file within this
# directory.
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(str, [""]),
    SECRET_KEY=(str, "s0m3-$upEr=S3cre7/|<3Y-L0n9Er=7hAn32(haR$"),
    DB_NAME=(str, "pylabber"),
    DB_USER=(str, "postgres"),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, "localhost"),
    DB_PORT=(int, 5432),
    RAW_SUBJECT_TABLE_PATH=(str, "subjects.xlsx"),
    QUESTIONNAIRE_DATA_PATH=(str, ""),
    APP_IP=(str, "localhost"),
    TESTING_MODE=(bool, False),
)
environ.Env.read_env()

# Fix notebook support for Django 3.0
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# The base directory of the project. Used to infer the locations of directories
# required by the application (static files, logs, etc).
BASE_DIR = str(Path(__file__).parent.parent.absolute())


####################
# Project settings #
####################

# Secret key used to provide cryptographic signing.
SECRET_KEY = env("SECRET_KEY")

# Debug mode switch (should be set to *True* in development and *False* in
# production).
DEBUG = env("DEBUG", default=True)

# List of safe hosts to serve.
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# List of applications used by the project.
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd Party
    "django_celery_beat",
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "corsheaders",
    "storages",
    "django_celery_results",
    "django_admin_inline_paginator",
    # Local
    "research",
    # Extensions
    "django_dicom",
    "django_mri",
    "django_analyses",
]

# List of hooks for request/response processing.
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Import path for the project's URLs configuration file.
ROOT_URLCONF = "pylabber.urls"

# A list of template engines used to render HTML pages.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ]
        },
    }
]

# Import path of the WSGI application object that Django’s built-in servers
# (e.g. *runserver*) will use.
WSGI_APPLICATION = "pylabber.wsgi.application"

# Databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Authentication
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Password strengh validation
VALIDATION_MODULE = "django.contrib.auth.password_validation"
SIMILARITY_VALIDATOR = f"{VALIDATION_MODULE}.UserAttributeSimilarityValidator"
MINIMUM_LENGTH_VALIDATOR = f"{VALIDATION_MODULE}.MinimumLengthValidator"
COMMON_PASSWORD_VALIDATOR = f"{VALIDATION_MODULE}.CommonPasswordValidator"
NUMERIC_PASSWORD_VALIDATOR = f"{VALIDATION_MODULE}.NumericPasswordValidator"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": SIMILARITY_VALIDATOR},
    {"NAME": MINIMUM_LENGTH_VALIDATOR},
    {"NAME": COMMON_PASSWORD_VALIDATOR},
    {"NAME": NUMERIC_PASSWORD_VALIDATOR},
]

# Media directory
MEDIA_ROOT = env("MEDIA_ROOT", default=os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
os.makedirs(STATIC_ROOT, exist_ok=True)
STATIC_URL = "/static/"
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
for static_files_dir in STATICFILES_DIRS:
    os.makedirs(static_files_dir, exist_ok=True)

# AWS S3 configuration
if os.getenv("USE_S3"):
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_REGION_NAME = "eu-central-1"

    # s3 static settings
    # AWS_LOCATION = "static"
    # STATIC_LOCATION = "static"
    # STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    # STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, "mysite/static"),
    # ]

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "pylabber.storage_backends.MediaStorage"

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Date format
DATE_FORMAT = "d/m/Y"

# Time format
TIME_FORMAT = "H:i:s"

# Datetime format
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Time zone
USE_TZ = True
TIME_ZONE = "Asia/Jerusalem"


# Logging
LOGGING_ROOT = os.path.join(BASE_DIR, "logs")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "format": "{asctime} {name} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "debug.log"),
            "maxBytes": 2048000,
            "backupCount": 5,
            "formatter": "normal",
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "info.log"),
            "maxBytes": 2048000,
            "backupCount": 5,
            "formatter": "normal",
        },
        "warning_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "warnings.log"),
            "maxBytes": 2048000,
            "backupCount": 2,
            "formatter": "normal",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["debug_file"],
            "propagate": True,
            "level": "DEBUG",
        },
        "data": {
            "handlers": ["debug_file", "info_file", "warning_file", "console"],
            "level": "DEBUG",
        },
        "data_import": {
            "handlers": ["debug_file", "info_file", "warning_file", "console"],
            "level": "DEBUG",
        },
        "analysis_exection": {
            "handlers": ["console", "info_file", "debug_file", "warning_file"],
            "level": "DEBUG",
        },
    },
}

########################
# Application settings #
########################

# Django REST Framework

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "pylabber.views.pagination.StandardResultsSetPagination",  # noqa: E501
    "PAGE_SIZE": 20,
    # djangorestframework-camel-case settings
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.serializers.UserSerializer"
}
CORS_ORIGIN_WHITELIST = [
    f"http://{env('APP_IP')}:8080",
    f"https://{env('APP_IP')}:8080",
    "http://localhost:8080",
    "https://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5006",
    "http://127.0.0.1:5006",
    "https://vuelabber.herokuapp.com",
    "https://pylabber.herokuapp.com",
]

# research
SUBJECT_MODEL = "research.Subject"
STUDY_GROUP_MODEL = "research.Group"
MEASUREMENT_MODEL = "research.MeasurementDefinition"
RAW_SUBJECT_TABLE_PATH = env("RAW_SUBJECT_TABLE_PATH")
QUESTIONNAIRE_DATA_PATH = env("QUESTIONNAIRE_DATA_PATH")
DATA_ACQUISITION_MODELS = [{"app_label": "django_mri", "model": "session"}]
# SSH_RSA_KEY = os.path.expanduser("~/.ssh/id_rsa")
SSH_KNOWN_HOSTS = os.path.expanduser("~/.ssh/known_hosts")

# django_analyses
ANALYSIS_INTERFACES = interfaces
ANALYSIS_BASE_PATH = os.path.join(MEDIA_ROOT, "analysis")
# ANALYSIS_VISUALIZERS = MRI_VISUALIZERS
EXTRA_INPUT_DEFINITION_SERIALIZERS = {
    "ScanInputDefinition": (
        "django_mri.serializers.input.scan_input_definition",
        "ScanInputDefinitionSerializer",
    ),
    "NiftiInputDefinition": (
        "django_mri.serializers.input.nifti_input_definition",
        "NiftiInputDefinitionSerializer",
    ),
}
EXTRA_INPUT_SERIALIZERS = {
    "ScanInput": (
        "django_mri.serializers.input.scan_input",
        "ScanInputSerializer",
    ),
    "NiftiInput": (
        "django_mri.serializers.input.nifti_input",
        "NiftiInputSerializer",
    ),
}
EXTRA_OUTPUT_DEFINITION_SERIALIZERS = {
    "NiftiOutputDefinition": (
        "django_mri.serializers.output.nifti_output_definition",
        "NiftiOutputDefinitionSerializer",
    ),
}
EXTRA_OUTPUT_SERIALIZERS = {
    "NiftiOutput": (
        "django_mri.serializers.output.nifti_output",
        "NiftiOutputSerializer",
    )
}

# django_mri
DATA_SHARE_ROOT = "/mnt/"

# django_dicom
DICOM_IMPORT_MODE = "minimal"

# For external usage of APP_IP
APP_IP = env("APP_IP")

TESTING_MODE = env("TESTING_MODE")

# Load Heroku environment settings.
# if not DEBUG:
#     DEBUG_PROPAGATE_EXCEPTIONS = True
#     django_heroku.settings(locals())


# Celery

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_EXPIRES = 0

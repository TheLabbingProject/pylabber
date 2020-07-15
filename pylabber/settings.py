"""
Django settings for pylabber project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ
import os

from django_mri.analysis.interfaces import interfaces
from pathlib import Path


###############
# Environment #
###############

# Environment variables are expected to be set in a .env file within this
# directory.
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(str, "s0m3-$upEr=S3cre7"),
    DB_NAME=(str, "pylabber"),
    DB_USER=(str, "postgres"),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, "localhost"),
    DB_PORT=(int, 5432),
    RAW_SUBJECT_TABLE_PATH=(str, "subjects.xlsx"),
    APP_IP=(str, "127.0.0.1"),
)
environ.Env.read_env()

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
DEBUG = env("DEBUG")

# List of safe hosts to serve.
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# List of applications used by the project.
INSTALLED_APPS = [
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd Party
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "corsheaders",
    # Local
    "research",
    # Extensions
    "django_dicom",
    "django_mri",
    "django_analyses",
]

# List of hooks for request/response processing.
MIDDLEWARE = [
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
MEDIA_ROOT = env("MEDIA_ROOT")
MEDIA_URL = "/media/"

# Static directory
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Date format
DATE_FORMAT = "d/m/Y"

# Time format
TIME_FORMAT = "H:i:s"

# Logging
LOGGING_ROOT = os.path.join(BASE_DIR, "logs")
LOGGING = {
    "version": 1,
    "formatters": {
        "normal": {"format": "{asctime} {name} {levelname} {message}", "style": "{",},
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "debug.log"),
            "maxBytes": 2048000,
            "backupCount": 5,
            "formatter": "normal",
            "filters": ["require_debug_true"],
        },
        "warning_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "warnings.log"),
            "maxBytes": 2048000,
            "backupCount": 2,
            "formatter": "normal",
        },
        "console": {"level": "WARNING", "class": "logging.StreamHandler"},
    },
    "loggers": {
        "data": {
            "handlers": ["debug_file", "warning_file", "console"],
            "level": "DEBUG",
        },
        "data_import": {
            "handlers": ["debug_file", "warning_file", "console"],
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
    "http://localhost:5006",
]


# research
SUBJECT_MODEL = "research.Subject"
STUDY_GROUP_MODEL = "research.Group"
RAW_SUBJECT_TABLE_PATH = env("RAW_SUBJECT_TABLE_PATH")

# django_analyses
ANALYSIS_INTERFACES = interfaces
ANALYSIS_BASE_PATH = os.path.join(MEDIA_ROOT, "analysis")
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
    "ScanInput": ("django_mri.serializers.input.scan_input", "ScanInputSerializer",),
    "NiftiInput": ("django_mri.serializers.input.nifti_input", "NiftiInputSerializer",),
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

# django_dicom
DICOM_IMPORT_MODE = "minimal"

# For external usage of APP_IP
APP_IP = env("APP_IP")

import os

from .settings import *

RAW_SUBJECT_TABLE_PATH = os.path.join(
    "research", "tests", "models", "test_subjects.xlsx"
)
MEDIA_ROOT = os.path.join(BASE_DIR, "test_media")
TESTS = True
TESTING_MODE = True

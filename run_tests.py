import os
import shutil
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "pylabber.test_settings"
    django.setup()
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["accounts", "research"])
    shutil.rmtree(settings.MEDIA_ROOT)
    sys.exit(bool(failures))

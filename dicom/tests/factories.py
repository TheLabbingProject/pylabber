import glob
import factory
import os

from dicom.models import Instance

TEST_FILES_PATH = './dicom/tests/files/'
SERIES_DIR = os.path.abspath(os.path.join(TEST_FILES_PATH, 'whole_series'))
SERIES_FILES = glob.glob(os.path.join(SERIES_DIR, '*.dcm'))


def get_test_file_path(name: str) -> str:
    file_path = os.path.join(TEST_FILES_PATH, f'{name}.dcm')
    return os.path.abspath(file_path)


class InstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instance
        strategy = factory.BUILD_STRATEGY

    file = factory.django.FileField()

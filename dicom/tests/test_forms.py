import os

from dicom.forms import CreateInstancesForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

TEST_FILE_PATH = os.path.abspath('./dicom/tests/files/test.dcm')


class FormTestCase(TestCase):
    def test_dcm_file_selection(self):
        with open(TEST_FILE_PATH, 'rb') as test_file:
            file_dict = {
                'dcm_files': SimpleUploadedFile(test_file.name,
                                                test_file.read())
            }
            form = CreateInstancesForm(files=file_dict)
            self.assertTrue(form.is_valid())

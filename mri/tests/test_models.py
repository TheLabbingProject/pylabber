from django.test import TestCase
# from mri.models import Scan
from mri.tests.factories import ScanFactory


class ScanModelTestCase(TestCase):
    def setUp(self):
        self.scan = ScanFactory.create()

    def test_default_nifti_name(self):
        name = self.scan.get_default_nifti_name()
        expected = f"{self.scan.id}"
        self.assertEqual(name, expected)


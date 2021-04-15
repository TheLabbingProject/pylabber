from django.test import TestCase
from django.urls import reverse

from ..factories import MeasurementDefinitionFactory


class MeasurementDefinitionModelTestCase(TestCase):
    def setUp(self):
        self.test_measure = MeasurementDefinitionFactory()
        self.test_measure.save()

    def test_get_absolute_url(self):
        expected = reverse(
            "research:measurement-detail", args=[str(self.test_measure.id)],
        )
        result = self.test_measure.get_absolute_url()
        self.assertEqual(result, expected)

    def test_str(self):
        value = str(self.test_measure)
        expected = self.test_measure.title
        self.assertEqual(value, expected)

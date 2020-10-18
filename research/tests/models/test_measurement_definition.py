from django.test import TestCase
from ..factories import MeasurementDefinitionFactory
from django.urls import reverse


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
        expected = f"{self.test_measure.title}|{self.test_measure.description}"
        self.assertEqual(str(self.test_measure), expected)

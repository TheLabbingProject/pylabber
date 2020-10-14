from django.test import TestCase
from ..factories import (
    MeasurementDefinitionFactory,
    TaskFactory,
    ProcedureFactory,
)
from django.urls import reverse


class ProcedureModelTestCase(TestCase):
    def setUp(self):
        self.test_procedure = ProcedureFactory()
        self.test_procedure.save()

    def test_get_absolute_url(self):
        expected = reverse(
            "research:procedure-detail", args=[str(self.test_procedure.id)],
        )
        result = self.test_procedure.get_absolute_url()
        self.assertEqual(result, expected)

    def test_str(self):
        expected = (
            f"{self.test_procedure.title}|{self.test_procedure.description}"
        )
        self.assertEqual(str(self.test_procedure), expected)

    def test_add_event(self):
        self.test_procedure.add_event(TaskFactory.create())
        self.test_procedure.add_event(MeasurementDefinitionFactory.create())
        self.assertEqual(len(self.test_procedure.events.all()), 2)
        self.assertEqual(self.test_procedure.index, 2)

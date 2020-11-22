from django.test import TestCase
from research.tests.factories import (
    ProcedureFactory,
    ProcedureStepFactory,
)
from research.models import Procedure
from django.urls import reverse


class ProcedureStepModelTestCase(TestCase):
    def setUp(self):
        self.procedure = ProcedureFactory.create()
        self.test_step = ProcedureStepFactory.create(procedure=self.procedure)

    def test_get_absolute_url(self):
        expected = reverse(
            "research:procedure_step-detail", args=[str(self.test_step.id)],
        )
        result = self.test_step.get_absolute_url()
        self.assertEqual(result, expected)

    def test_procedure_fk(self):
        result = self.test_step.procedure
        self.assertIsInstance(result, Procedure)
        self.assertEqual(result, self.procedure)

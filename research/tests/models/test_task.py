from django.test import TestCase
from django.urls import reverse

from ..factories import TaskFactory


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.test_task = TaskFactory()
        self.test_task.save()

    def test_get_absolute_url(self):
        expected = reverse(
            "research:task-detail", args=[str(self.test_task.id)]
        )
        result = self.test_task.get_absolute_url()
        self.assertEqual(result, expected)

    def test_str(self):
        value = str(self.test_task)
        expected = self.test_task.title
        self.assertEqual(value, expected)

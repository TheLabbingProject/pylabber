from django.test import TestCase
from ..factories import TaskFactory
from django.urls import reverse


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
        expected = f"{self.test_task.title}|{self.test_task.description}"
        self.assertEqual(str(self.test_task), expected)

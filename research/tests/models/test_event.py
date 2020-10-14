from django.test import TestCase
from ..factories import EventFactory
from django.urls import reverse


class EventModelTestCase(TestCase):
    def setUp(self):
        self.test_event = EventFactory()
        self.test_event.save()

    def test_get_absolute_url(self):
        expected = reverse(
            "research:event-detail", args=[str(self.test_event.id)]
        )
        result = self.test_event.get_absolute_url()
        self.assertEqual(result, expected)

    def test_str(self):
        expected = f"{self.test_event.title}|{self.test_event.description}"
        self.assertEqual(str(self.test_event), expected)

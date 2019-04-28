from django.apps import apps
from django.test import TestCase
from research.apps import ResearchConfig


class ResearchConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ResearchConfig.name, "research")
        self.assertEqual(apps.get_app_config("research").name, "research")


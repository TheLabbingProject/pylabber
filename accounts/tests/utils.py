from django.test import TestCase
from .factories import UserFactory, TEST_PASSWORD


class MockRequest:
    pass


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(password=TEST_PASSWORD)
        self.user.save()
        self.login()

    def login(self):
        self.client.login(username=self.user.username, password=TEST_PASSWORD)

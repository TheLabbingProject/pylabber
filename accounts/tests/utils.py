# from django.test import TestCase
from rest_framework.test import APITestCase

# from .factories import TEST_PASSWORD  # UserFactory,
from django.contrib.auth import get_user_model

TEST_PASSWORD = "Aa123456"
User = get_user_model()


class MockRequest:
    pass


class LoggedInTestCase(APITestCase):
    def setUp(self):
        # self.user = UserFactory(password=TEST_PASSWORD)
        self.user = User.objects.create_user(
            username="test", email="test@test.test", password=TEST_PASSWORD
        )
        self.user.save()
        self.login()

    def login(self):
        self.client.login(username=self.user.username, password=TEST_PASSWORD)

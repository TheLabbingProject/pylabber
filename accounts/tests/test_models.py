from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase

from .fixtures import UserFactory

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_new_user(self):
        user = UserFactory()
        self.assertIs(type(user), User)

    def test_authenticate_user_with_username_and_password(self):
        user = UserFactory()
        authenticated_user = authenticate(
            username=user.username, password=user._password)
        self.assertEqual(user, authenticated_user)

    def test_authenticate_user_with_email_and_password(self):
        user = UserFactory()
        authenticated_user = authenticate(
            email=user.email, password=user._password)
        self.assertEqual(user, authenticated_user)

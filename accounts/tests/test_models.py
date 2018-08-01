from accounts.models import User, Profile
from django.test import TestCase
from .factories import UserFactory


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_created_with_profile(self):
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user.profile, Profile)


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = self.user.profile

    def test_str(self):
        self.assertEqual(str(self.profile), self.user.get_full_name())

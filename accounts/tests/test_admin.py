from accounts.admin import UserAdmin, ProfileInline
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from .factories import UserFactory
from .utils import MockRequest

User = get_user_model()


class AdminTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)


class UserAdminTestCase(AdminTestCase):
    def test_get_user_institute(self):
        self.assertEqual(
            self.user.profile.institute, self.user_admin.get_institute(self.user)
        )

    def test_get_profile_inline_with_instance(self):
        request = MockRequest()
        request.user = self.user
        inlines = self.user_admin.get_inline_instances(request, self.user)
        self.assertIsInstance(inlines[0], ProfileInline)
        self.assertEqual(len(inlines), 2)

    def test_get_profile_inline_without_instance(self):
        request = MockRequest()
        request.user = self.user
        inlines = self.user_admin.get_inline_instances(request)
        self.assertEqual(inlines, [])

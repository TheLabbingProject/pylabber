from accounts.models.choices import Title
from accounts.models import User, Profile
from django.test import TestCase
from .factories import UserFactory, TEST_PASSWORD


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_user_created_with_profile(self):
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user.profile, Profile)


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile = self.user.profile
        self.titleless_user = UserFactory.build(profile__title="")

    def test_profile_is_created_when_user_is_saved(self):
        self.assertTrue(Profile.objects.count() == 1)
        self.titleless_user.save()
        self.assertTrue(Profile.objects.count() == 2)

    def test_str(self):
        self.assertEqual(str(self.profile), self.user.get_full_name())

    def test_login(self):
        result = self.client.login(username=self.user.username, password=TEST_PASSWORD)
        self.assertTrue(result)

    def test_full_name_with_title(self):
        name = self.profile.get_full_name()
        user_full_name = self.user.get_full_name()
        title = Title[self.profile.title].value
        expected = f"{user_full_name}, {title}"
        self.assertEqual(name, expected)

    def test_full_name_without_title(self):
        name = self.titleless_user.profile.get_full_name()
        user_full_name = self.titleless_user.get_full_name()
        self.assertEqual(name, user_full_name)

    # def test_get_absolute_url_when_logged_out(self):
    #     self.client.logout()
    #     url = self.profile.get_absolute_url()
    #     response = self.client.post(url)
    #     expected = f"/accounts/login/?next=/accounts/{self.user.id}/"
    #     self.assertRedirects(
    #         response,
    #         expected,
    #         status_code=302,
    #         target_status_code=200,
    #         msg_prefix="",
    #         fetch_redirect_response=True,
    #     )

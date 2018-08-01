# from django.test import TestCase
# from .factories import UserFactory, TEST_PASSWORD

# class EmailModelBackendTestCase(TestCase):
#     def setUp(self):
#         self.user = UserFactory(password=TEST_PASSWORD)
#         self.user.save()

#     def login_with_email(self):
#         return self.client.login(email=self.user.email, password=TEST_PASSWORD)

#     def login_with_username(self):
#         return self.client.login(
#             username=self.user.username, password='asdfsadf')

#     def test_login_with_email(self):
#         logged_in = self.login_with_email()
#         self.assertTrue(logged_in)
#         self.client.logout()

#     def test_login_with_username(self):
#         logged_in = self.login_with_username()
#         self.assertTrue(logged_in)
#         self.client.logout()

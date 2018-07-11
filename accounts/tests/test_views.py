import os
import platform

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver

from .fixtures import UserFactory


class LoginPageTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ------------------------------------
        # set up Selenium WebDriver for Chrome
        # ------------------------------------

        # asking Python which OS we're using
        system = platform.system()

        # find the right ChromeDriver executable, based on the host OS
        if system == 'Windows':
            filename = 'chromedriver_win32.exe'
        elif system == 'Linux':
            filename = 'chromedriver_linux64'
        elif system == 'Darwin':  # Max OS X
            filename = 'chromedriver_mac64'

        executable_path = os.path.join(settings.BASE_DIR, 'selenium', filename)

        # instantiate Selenium
        cls.browser = webdriver.Chrome(executable_path=executable_path)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_submit_with_invalid_email_and_password_combination(self):
        # first, create new user
        user = UserFactory()

        # go the the login page
        login_page = self.live_server_url + reverse('accounts:login')
        self.browser.get(login_page)

        # grab the form and its input elements
        form = self.browser.find_element_by_tag_name('form')
        email_field = form.find_element_by_name('email')
        password_field = form.find_element_by_name('password')

        email_field.send_keys(user.email)

        # "accidentally" drop the last character in the password
        wrong_password = user._password[:-1]
        password_field.send_keys(wrong_password)

        # submit the form, then expect for an error message
        form.submit()

        error_list = self.browser \
            .find_element_by_css_selector('.ui.negative.message')

        error_message = error_list.find_element_by_tag_name('li')
        expected_error_message = 'Invalid e-mail / password combination'

        self.assertEqual(error_message.text, expected_error_message)

import os

from accounts.tests.utils import TEST_USER_DICT
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from dicom.models import Instance
from shutil import copyfile
from .test_models import TEST_FILES_PATH

TEST_FILE_NAME = 'test.dcm'
TEST_FILE_PATH = os.path.abspath(os.path.join(TEST_FILES_PATH, TEST_FILE_NAME))


class InstanceViewTestCase(TestCase):
    def create_test_instance(self):
        dest = os.path.join(settings.MEDIA_ROOT, TEST_FILE_NAME)
        copyfile(TEST_FILE_PATH, dest)
        try:
            return Instance.objects.create(file=TEST_FILE_NAME)
        except Exception as e:
            self.fail(
                f'Failed to create test instance with the following exception:\n{e}'
            )

    def get_test_instance(self):
        try:
            return Instance.objects.get(id=1)
        except Exception as e:
            self.fail(f'Failed to retrieve test instance with the following\
                 exception:\n{e}')


class LoggedOutInstanceViewTestCase(InstanceViewTestCase):
    def setUp(self):
        self.test_instance = self.create_test_instance()

    def test_instance_list_redirects_to_login(self):
        url = reverse('instance_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_instance_detail_redirects_to_login(self):
        url = self.test_instance.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_instances_create_redirects_to_login(self):
        url = reverse('instances_create')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInInstanceViewTestCase(InstanceViewTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(**TEST_USER_DICT)
        self.test_instance = self.create_test_instance()
        self.login()

    def login(self):
        username = TEST_USER_DICT['username']
        password = TEST_USER_DICT['password']
        self.client.login(username=username, password=password)

    def test_list_view(self):
        response = self.client.get(reverse('instance_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instances/instance_list.html')

    def test_detail_view(self):
        url = self.test_instance.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instances/instance_detail.html')

    def test_create_view(self):
        url = reverse('instances_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instances/instances_create.html')

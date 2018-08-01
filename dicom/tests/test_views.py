import os

from accounts.tests.utils import LoggedInTestCase
from django.test import TestCase
from django.urls import reverse
from .factories import InstanceFactory, get_test_file_path


class LoggedOutInstanceViewTestCase(TestCase):
    def setUp(self):
        self.test_instance = InstanceFactory(
            file__from_path=get_test_file_path('test'))
        self.test_instance.save()

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


class LoggedInInstanceViewTestCase(LoggedInTestCase):
    def setUp(self):
        self.test_instance = InstanceFactory(
            file__from_path=get_test_file_path('test'))
        self.test_instance.save()
        super(LoggedInInstanceViewTestCase, self).setUp()

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

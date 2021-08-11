from accounts.tests.utils import LoggedInTestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..factories import StudyFactory


class LoggedOutStudyViewTestCase(TestCase):
    def setUp(self):
        self.test_study = StudyFactory()
        self.test_study.save()

    def test_study_list_redirects_to_login(self):
        url = reverse("research:study-list")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_study_detail_redirects_to_login(self):
        url = self.test_study.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_study_update_redirects_to_login(self):
        url = self.test_study.get_absolute_url()
        study = StudyFactory()
        args = {
            "title": study.title,
            "description": study.description,
        }
        response = self.client.patch(url, data=args, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_study_delete_redirects_to_login(self):
        url = self.test_study.get_absolute_url()
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_study_create_redirects_to_login(self):
        url = reverse("research:study-list")
        study = StudyFactory()
        args = {
            "title": study.title,
            "description": study.description,
            "modified": study.modified,
        }
        response = self.client.post(url, data=args, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoggedInStudyViewTestCase(LoggedInTestCase):
    def setUp(self):
        self.test_study = StudyFactory()
        self.test_study.save()
        super(LoggedInStudyViewTestCase, self).setUp()

    def test_list_view(self):
        response = self.client.get(reverse("research:study-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_detail_view(self):
    #     url = self.test_study.get_absolute_url()
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_view(self):
    #     url = self.test_study.get_absolute_url()
    #     study = StudyFactory()
    #     args = {
    #         "title": study.title,
    #         "description": study.description,
    #     }
    #     response = self.client.patch(url, data=args)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_view(self):
    #     url = self.test_study.get_absolute_url()
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_view(self):
        url = reverse("research:study-list")
        study = StudyFactory()
        args = {
            "title": study.title,
            "description": study.description,
            "modified": study.modified,
        }
        response = self.client.post(url, data=args)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

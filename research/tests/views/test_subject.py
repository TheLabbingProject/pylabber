from accounts.tests.utils import LoggedInTestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..factories import SubjectFactory


class LoggedOutSubjectViewTestCase(TestCase):
    def setUp(self):
        self.test_subject = SubjectFactory()
        self.test_subject.save()

    def test_subject_list_redirects_to_login(self):
        url = reverse("research:subject-list")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_detail_redirects_to_login(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_update_redirects_to_login(self):
        url = self.test_subject.get_absolute_url()
        subject = SubjectFactory()
        args = {
            "first_name": subject.first_name,
            "last_name": subject.last_name,
        }
        response = self.client.patch(url, data=args, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_delete_redirects_to_login(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_create_redirects_to_login(self):
        url = reverse("research:subject-list")
        subject = SubjectFactory()
        args = {
            "id_number": subject.id_number,
            "first_name": subject.first_name,
            "last_name": subject.last_name,
            "date_of_birth": subject.date_of_birth,
            "dominant_hand": subject.dominant_hand,
            "sex": subject.sex,
            "gender": subject.gender,
        }
        response = self.client.post(url, data=args, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoggedInSubjectViewTestCase(LoggedInTestCase):
    def setUp(self):
        self.test_subject = SubjectFactory()
        self.test_subject.save()
        super(LoggedInSubjectViewTestCase, self).setUp()

    def test_list_view(self):
        response = self.client.get(reverse("research:subject-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_view(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_view(self):
        url = self.test_subject.get_absolute_url()
        subject = SubjectFactory()
        args = {
            "first_name": subject.first_name,
            "last_name": subject.last_name,
        }
        response = self.client.patch(url, data=args)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_view(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_view(self):
        url = reverse("research:subject-list")
        subject = SubjectFactory()
        args = {
            "id_number": subject.id_number,
            "first_name": subject.first_name,
            "last_name": subject.last_name,
            "date_of_birth": subject.date_of_birth,
            "dominant_hand": subject.dominant_hand,
            "sex": subject.sex,
            "gender": subject.gender,
        }
        response = self.client.post(url, data=args)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

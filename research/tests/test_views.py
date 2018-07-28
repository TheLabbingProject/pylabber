from accounts.tests.utils import TEST_USER_DICT
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from research.models import Study, Subject
from .test_models import TEST_STUDY_DICT, TEST_SUBJECT_DICT


class StudyViewTestCase(TestCase):
    def create_test_study(self):
        try:
            return Study.objects.create(**TEST_STUDY_DICT)
        except Exception as e:
            self.fail(
                f'Failed to create test study with the following exception:\n{e}'
            )

    def get_test_study(self):
        try:
            return Study.objects.get(id=1)
        except Exception as e:
            self.fail(
                f'Failed to retrieve test study with the following exception:\n{e}'
            )


class LoggedOutStudyViewTestCase(StudyViewTestCase):
    def setUp(self):
        self.test_study = self.create_test_study()

    def test_study_list_redirects_to_login(self):
        url = reverse('study_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_study_detail_redirects_to_login(self):
        url = self.test_study.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_study_update_redirects_to_login(self):
        url = self.test_study.get_absolute_url() + 'edit/'
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_study_delete_redirects_to_login(self):
        url = self.test_study.get_absolute_url() + 'delete/'
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_study_create_redirects_to_login(self):
        url = reverse('study_create')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInStudyViewTestCase(StudyViewTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(**TEST_USER_DICT)
        self.test_study = self.create_test_study()
        self.login()

    def login(self):
        username = TEST_USER_DICT['username']
        password = TEST_USER_DICT['password']
        self.client.login(username=username, password=password)

    def test_list_view(self):
        response = self.client.get(reverse('study_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies/study_list.html')

    def test_detail_view(self):
        url = self.test_study.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies/study_detail.html')

    def test_update_view(self):
        url = self.test_study.get_absolute_url() + 'edit/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies/study_update.html')

    def test_delete_view(self):
        url = self.test_study.get_absolute_url() + 'delete/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies/study_delete.html')

    def test_create_view(self):
        url = reverse('study_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies/study_create.html')


class SubjectViewTestCase(TestCase):
    def create_test_subject(self):
        try:
            return Subject.objects.create(**TEST_SUBJECT_DICT)
        except Exception as e:
            self.fail(
                f'Failed to create test subject with the following exception:\n{e}'
            )

    def get_test_subject(self):
        try:
            return Subject.objects.get(id=1)
        except Exception as e:
            self.fail(
                f'Failed to retrieve test subject with the following exception:\n{e}'
            )


class LoggedOutSubjectViewTestCase(SubjectViewTestCase):
    def setUp(self):
        self.test_subject = self.create_test_subject()

    def test_subject_list_redirects_to_login(self):
        url = reverse('subject_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_subject_detail_redirects_to_login(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_subject_update_redirects_to_login(self):
        url = self.test_subject.get_absolute_url() + 'edit/'
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_subject_delete_redirects_to_login(self):
        url = self.test_subject.get_absolute_url() + 'delete/'
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_subject_create_redirects_to_login(self):
        url = reverse('subject_create')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInSubjectViewTestCase(SubjectViewTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(**TEST_USER_DICT)
        self.test_subject = self.create_test_subject()
        self.login()

    def login(self):
        username = TEST_USER_DICT['username']
        password = TEST_USER_DICT['password']
        self.client.login(username=username, password=password)

    def test_list_view(self):
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_list.html')

    def test_detail_view(self):
        url = self.test_subject.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_detail.html')

    def test_update_view(self):
        url = self.test_subject.get_absolute_url() + 'edit/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_update.html')

    def test_delete_view(self):
        url = self.test_subject.get_absolute_url() + 'delete/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_delete.html')

    def test_create_view(self):
        url = reverse('subject_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_create.html')

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
        self.assertTemplateUsed(response, 'dicom/instances/instance_list.html')

    def test_detail_view(self):
        url = self.test_instance.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'dicom/instances/instance_detail.html')

    def test_create_view(self):
        url = reverse('instances_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'dicom/instances/instances_create.html')


class LoggedOutSeriesViewTestCase(TestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_series = instance.series

    def test_series_list_redirects_to_login(self):
        url = reverse('series_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_series_detail_redirects_to_login(self):
        url = self.test_series.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInSeriesViewTestCase(LoggedInTestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_series = instance.series
        super(LoggedInSeriesViewTestCase, self).setUp()

    def test_list_view(self):
        response = self.client.get(reverse('series_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/series/series_list.html')

    def test_detail_view(self):
        url = self.test_series.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/series/series_detail.html')


class LoggedOutPatientViewTestCase(TestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_patient = instance.patient

    def test_patient_list_redirects_to_login(self):
        url = reverse('patient_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_patient_detail_redirects_to_login(self):
        url = self.test_patient.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInPatientViewTestCase(LoggedInTestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_patient = instance.patient
        super(LoggedInPatientViewTestCase, self).setUp()

    def test_list_view(self):
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/patients/patient_list.html')

    def test_detail_view(self):
        url = self.test_patient.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/patients/patient_detail.html')


class LoggedOutStudyViewTestCase(TestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_study = instance.study

    def test_study_list_redirects_to_login(self):
        url = reverse('dicom_study_list')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_study_detail_redirects_to_login(self):
        url = self.test_study.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class LoggedInStudyViewTestCase(LoggedInTestCase):
    def setUp(self):
        instance = InstanceFactory(file__from_path=get_test_file_path('test'))
        instance.save()
        self.test_study = instance.study
        super(LoggedInStudyViewTestCase, self).setUp()

    def test_list_view(self):
        response = self.client.get(reverse('dicom_study_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/studies/study_list.html')

    def test_detail_view(self):
        url = self.test_study.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dicom/studies/study_detail.html')
import numpy as np
import os
import pydicom

from datetime import date, time
from django.core.files.uploadedfile import SimpleUploadedFile
from dicom.models import Instance
from django.test import TestCase
from .factories import (
    InstanceFactory,
    get_test_file_path,
    TEST_FILES_PATH,
    SERIES_FILES,
)


class InstanceModelTestCase(TestCase):
    TEST_INSTANCES = [
        'test',
        'same_series',
        'different_series',
        'different_study_same_patient',
        # 'different_patient_same_study',
        'different_patient_different_study',
    ]

    ZIPPED_UIDS = [
        '1.3.12.2.1107.5.2.43.66024.2016120813301385447497555',
        '1.3.12.2.1107.5.2.43.66024.2016120813360043323300309',
        '1.3.12.2.1107.5.2.43.66024.2016120813262299647895751',
        '1.3.12.2.1107.5.2.43.66024.2016121412432166520775187',
        '1.3.12.2.1107.5.2.43.66024.201612141317482895906735',
        '1.3.12.2.1107.5.2.43.66024.2016121412485542898477604',
    ]

    def setUp(self):
        self.create_all_test_instances()

    def load_uploaded_dcm(self):
        with open(get_test_file_path('from_file'), 'rb') as test_file:
            return SimpleUploadedFile(test_file.name, test_file.read())

    def load_uploaded_zip(self):
        relative_path = os.path.join(TEST_FILES_PATH, 'test.zip')
        source = os.path.abspath(relative_path)
        with open(source, 'rb') as test_zip:
            return SimpleUploadedFile(test_zip.name, test_zip.read())

    def create_all_test_instances(self):
        for name in self.TEST_INSTANCES:
            path = get_test_file_path(name)
            instance = InstanceFactory(file__from_path=path)
            instance.save()

    def get_instance(self, name: str) -> Instance:
        id = self.TEST_INSTANCES.index(name) + 1
        return Instance.objects.get(id=id)

    def test_str(self):
        self.assertEqual(
            str(self.test_instance), self.test_instance.headers.SOPInstanceUID)

    def test_get_instance_data(self):
        data = self.test_instance.read_data()
        self.assertIsInstance(data, pydicom.dataset.FileDataset)
        self.assertTrue(hasattr(data, 'pixel_array'))

    def test_get_instance_headers(self):
        data = self.test_instance.read_headers()
        self.assertIsInstance(data, pydicom.dataset.FileDataset)
        with self.assertRaises(TypeError):
            data.pixel_array

    def test_instance_uid(self):
        self.assertEqual(self.test_instance.instance_uid,
                         self.test_instance.headers.SOPInstanceUID)

    def test_instance_number(self):
        self.assertEqual(self.test_instance.number,
                         self.test_instance.headers.InstanceNumber)

    def test_instance_date(self):
        self.assertEqual(self.test_instance.date, date(2016, 12, 8))

    def test_instance_time(self):
        self.assertEqual(self.test_instance.time, time(13, 11, 9, 254000))

    def test_series_creation(self):
        self.assertIsNotNone(self.test_instance.series)

    def test_series_uid(self):
        new_series_uid = self.test_instance.series.series_uid
        expected_uid = self.test_instance.headers.SeriesInstanceUID
        self.assertEqual(new_series_uid, expected_uid)

    def test_series_number(self):
        self.assertEqual(self.test_instance.series.number,
                         self.test_instance.headers.SeriesNumber)

    def test_series_date(self):
        self.assertEqual(self.test_instance.series.date, date(2016, 12, 8))

    def test_series_time(self):
        self.assertEqual(self.test_instance.series.time, time(
            13, 11, 9, 251000))

    def test_series_description(self):
        self.assertEqual(self.test_instance.series.description,
                         self.test_instance.headers.SeriesDescription)

    def test_study_creation(self):
        self.assertIsNotNone(self.test_instance.study)

    def test_series_study_is_instance_study(self):
        self.assertEqual(self.test_instance.study,
                         self.test_instance.series.study)

    def test_study_date(self):
        self.assertEqual(self.test_instance.study.date, date(2016, 12, 8))

    def test_study_time(self):
        self.assertEqual(self.test_instance.study.time, time(13, 5, 56, 90000))

    def test_study_description(self):
        self.assertEqual(self.test_instance.study.description,
                         self.test_instance.headers.StudyDescription)

    def test_patient_creation(self):
        self.assertIsNotNone(self.test_instance.patient)

    def test_series_patient_is_instance_patient(self):
        self.assertEqual(self.test_instance.patient,
                         self.test_instance.series.patient)

    def test_patient_uid(self):
        self.assertEqual(self.test_instance.patient.patient_uid,
                         self.test_instance.headers.PatientID)

    def test_patient_given_name(self):
        self.assertEqual(self.test_instance.patient.given_name,
                         self.test_instance.headers.PatientName.given_name)

    def test_patient_family_name(self):
        self.assertEqual(self.test_instance.patient.family_name,
                         self.test_instance.headers.PatientName.family_name)

    def test_patient_middle_name(self):
        self.assertEqual(self.test_instance.patient.middle_name,
                         self.test_instance.headers.PatientName.middle_name)

    def test_patient_name_prefix(self):
        self.assertEqual(self.test_instance.patient.name_prefix,
                         self.test_instance.headers.PatientName.name_prefix)

    def test_patient_name_suffix(self):
        self.assertEqual(self.test_instance.patient.name_suffix,
                         self.test_instance.headers.PatientName.name_suffix)

    def test_patient_birthdate(self):
        self.assertIsInstance(self.test_instance.patient.date_of_birth, date)

    def test_patient_sex(self):
        self.assertEqual(
            self.test_instance.patient.sex,
            Instance.SEX_DICT[self.test_instance.headers.PatientSex])

    def test_file_moved_to_default_location(self):
        default_location = self.test_instance.get_default_file_name()
        self.assertTrue(
            self.test_instance.file.path.endswith(default_location))

    def test_same_series_instance_has_same_series(self):
        self.assertEqual(self.test_instance.series,
                         self.same_series_instance.series)

    def test_same_series_instance_has_same_patient(self):
        self.assertEqual(self.test_instance.patient,
                         self.same_series_instance.patient)

    def test_same_series_instance_has_same_study(self):
        self.assertEqual(self.test_instance.study,
                         self.same_series_instance.study)

    def test_different_series_instance_has_different_series(self):
        self.assertNotEqual(self.test_instance.series,
                            self.different_series_instance.series)

    def test_different_series_instance_has_same_patient(self):
        self.assertEqual(self.test_instance.patient,
                         self.different_series_instance.patient)

    def test_different_series_instance_has_same_study(self):
        self.assertEqual(self.test_instance.study,
                         self.different_series_instance.study)

    def test_different_study_same_patient_instance_has_different_study(self):
        self.assertNotEqual(self.test_instance.study,
                            self.different_study_same_patient_instance.study)

    def test_different_study_same_patient_instance_has_same_patient(self):
        self.assertEqual(self.test_instance.patient,
                         self.different_study_same_patient_instance.patient)

    def test_different_patient_different_study_instance_has_different_patient(
            self):
        self.assertNotEqual(
            self.test_instance.patient,
            self.different_patient_different_study_instance.patient)

    def test_different_patient_different_study_instance_has_different_study(
            self):
        self.assertNotEqual(
            self.test_instance.study,
            self.different_patient_different_study_instance.study)

    def test_instance_creation_from_uploaded_dcm(self):
        uploaded_dcm = self.load_uploaded_dcm()
        instance = Instance.objects.from_dcm(uploaded_dcm)
        self.assertIsInstance(instance, Instance)
        self.assertIsNotNone(instance.instance_uid)

    def test_instances_creation_from_uploaded_zip(self):
        uploaded_zip = self.load_uploaded_zip()
        Instance.objects.from_zip(uploaded_zip)
        for uid in self.ZIPPED_UIDS:
            self.assertIsNotNone(Instance.objects.get(instance_uid=uid))

    @property
    def test_instance(self):
        return self.get_instance('test')

    @property
    def same_series_instance(self):
        return self.get_instance('same_series')

    @property
    def different_series_instance(self):
        return self.get_instance('different_series')

    @property
    def different_study_same_patient_instance(self):
        return self.get_instance('different_study_same_patient')

    # TODO: Add different patient same study test

    @property
    def different_patient_different_study_instance(self):
        return self.get_instance('different_patient_different_study')


class StudyModelTestCase(TestCase):
    def setUp(self):
        path = get_test_file_path('test')
        test_instance = InstanceFactory(file__from_path=path)
        test_instance.save()
        self.test_study = test_instance.study

    def test_str(self):
        self.assertEqual(str(self.test_study), self.test_study.study_uid)


class SeriesModelTestCase(TestCase):
    def setUp(self):
        for path in SERIES_FILES:
            instance = InstanceFactory(file__from_path=path)
            instance.save()
        self.test_series = instance.series

    def test_str(self):
        self.assertEqual(str(self.test_series), self.test_series.series_uid)

    def test_verbose_name(self):
        self.assertEqual(self.test_series._meta.verbose_name_plural, 'Series')

    def test_getting_data(self):
        data = self.test_series.get_data()
        self.assertIsInstance(data, np.ndarray)
        self.assertEqual(data.shape, (512, 512, 19))


class PatientModelTestCase(TestCase):
    def setUp(self):
        path = get_test_file_path('test')
        test_instance = InstanceFactory(file__from_path=path)
        test_instance.save()
        self.test_patient = test_instance.patient

    def test_str(self):
        self.assertEqual(str(self.test_patient), self.test_patient.patient_uid)

    def test_name_id(self):
        first_name = self.test_patient.given_name
        last_name = self.test_patient.family_name
        expected = f'{last_name[:2]}{first_name[:2]}'
        self.assertEqual(self.test_patient.get_name_id(), expected)

    def test_getting_subject_attributes(self):
        expected = {
            'first_name': self.test_patient.given_name,
            'last_name': self.test_patient.family_name,
            'date_of_birth': self.test_patient.date_of_birth,
            'sex': self.test_patient.sex,
            'id_number': self.test_patient.patient_uid,
        }
        self.assertEqual(self.test_patient.get_subject_attributes(), expected)

    def test_subject_created(self):
        self.assertIsNotNone(self.test_patient.subject)

    def test_get_subject_when_subject_field_is_set(self):
        self.assertEqual(self.test_patient.subject,
                         self.test_patient.get_subject())

    def test_find_subject_when_subject_does_not_exist(self):
        original_id = self.test_patient.patient_uid
        self.test_patient.patient_uid = '012345678'
        self.test_patient.save()
        self.assertIsNone(self.test_patient.find_subject())
        self.test_patient.patient_uid = original_id
        self.test_patient.save()

    def test_get_subject_when_subject_exists(self):
        subject = self.test_patient.subject
        self.test_patient.subject = None
        self.test_patient.save()
        self.assertIsNone(self.test_patient.subject)
        self.assertEqual(self.test_patient.get_subject(), subject)
        self.test_patient.subject = subject
        self.test_patient.save()

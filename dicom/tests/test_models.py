import os
import pydicom

from datetime import date, time
from django.conf import settings
from django.test import TestCase
from dicom.models import Instance
from shutil import copyfile

TEST_FILES_PATH = './dicom/tests/files/'


class InstanceModelTestCase(TestCase):
    TEST_INSTANCES = [
        'test',
        'same_series',
        'different_series',
        'different_study_same_patient',
        # 'different_patient_same_study',
        'different_patient_different_study',
    ]

    def setUp(self):
        self.raw = self.read_all_test_files()
        self.copy_all_test_files()
        self.create_all_test_instances()

    def get_test_file_path(self, name: str) -> str:
        file_path = os.path.join(TEST_FILES_PATH, f'{name}.dcm')
        return os.path.abspath(file_path)

    def get_test_file_dest(self, name: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, f'{name}.dcm')

    def copy_test_file(self, name: str) -> None:
        source = self.get_test_file_path(name)
        dest = self.get_test_file_dest(name)
        copyfile(source, dest)

    def create_test_instance(self, name: str) -> Instance:
        file = name + '.dcm'
        return Instance.objects.create(file=file)

    def read_test_file(self, name: str) -> pydicom.dataset.FileDataset:
        file_path = self.get_test_file_path(name)
        return pydicom.dcmread(file_path)

    def read_all_test_files(self):
        return {
            name: self.read_test_file(name)
            for name in self.TEST_INSTANCES
        }

    def copy_all_test_files(self):
        for name in self.TEST_INSTANCES:
            self.copy_test_file(name)

    def create_all_test_instances(self):
        for name in self.TEST_INSTANCES:
            self.create_test_instance(name)

    def delete_test_file_copies_and_clean_up(self):
        for name in self.TEST_INSTANCES:
            instance = self.get_instance(name)
            dir_path = os.path.dirname(instance.file.path)
            instance.file.delete()
            while dir_path != settings.MEDIA_ROOT:
                try:
                    os.rmdir(dir_path)
                except OSError:
                    break
                dir_path = os.path.dirname(dir_path)

    def get_instance(self, name: str) -> Instance:
        id = self.TEST_INSTANCES.index(name) + 1
        return Instance.objects.get(id=id)

    def test_headers_loaded_successfully(self):
        self.assertIsInstance(self.test_instance.headers,
                              pydicom.dataset.FileDataset)

    def test_str(self):
        self.assertEqual(
            str(self.test_instance), self.raw['test'].SOPInstanceUID)

    def test_instance_uid(self):
        self.assertEqual(self.test_instance.instance_uid,
                         self.raw['test'].SOPInstanceUID)

    def test_instance_number(self):
        self.assertEqual(self.test_instance.number,
                         self.raw['test'].InstanceNumber)

    def test_instance_date(self):
        self.assertEqual(self.test_instance.date, date(2016, 12, 8))

    def test_instance_time(self):
        self.assertEqual(self.test_instance.time, time(13, 11, 9, 254000))

    def test_series_creation(self):
        self.assertIsNotNone(self.test_instance.series)

    def test_series_uid(self):
        new_series_uid = self.test_instance.series.series_uid
        expected_uid = self.raw['test'].SeriesInstanceUID
        self.assertEqual(new_series_uid, expected_uid)

    def test_series_number(self):
        self.assertEqual(self.test_instance.series.number,
                         self.raw['test'].SeriesNumber)

    def test_series_date(self):
        self.assertEqual(self.test_instance.series.date, date(2016, 12, 8))

    def test_series_time(self):
        self.assertEqual(self.test_instance.series.time, time(
            13, 11, 9, 251000))

    def test_series_description(self):
        self.assertEqual(self.test_instance.series.description,
                         self.raw['test'].SeriesDescription)

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
                         self.raw['test'].StudyDescription)

    def test_patient_creation(self):
        self.assertIsNotNone(self.test_instance.patient)

    def test_series_patient_is_instance_patient(self):
        self.assertEqual(self.test_instance.patient,
                         self.test_instance.series.patient)

    def test_patient_uid(self):
        self.assertEqual(self.test_instance.patient.patient_uid,
                         self.raw['test'].PatientID)

    def test_patient_given_name(self):
        self.assertEqual(self.test_instance.patient.given_name,
                         self.raw['test'].PatientName.given_name)

    def test_patient_family_name(self):
        self.assertEqual(self.test_instance.patient.family_name,
                         self.raw['test'].PatientName.family_name)

    def test_patient_middle_name(self):
        self.assertEqual(self.test_instance.patient.middle_name,
                         self.raw['test'].PatientName.middle_name)

    def test_patient_name_prefix(self):
        self.assertEqual(self.test_instance.patient.name_prefix,
                         self.raw['test'].PatientName.name_prefix)

    def test_patient_name_suffix(self):
        self.assertEqual(self.test_instance.patient.name_suffix,
                         self.raw['test'].PatientName.name_suffix)

    def test_patient_birthdate(self):
        self.assertIsInstance(self.test_instance.patient.date_of_birth, date)

    def test_patient_sex(self):
        self.assertEqual(self.test_instance.patient.sex,
                         Instance.SEX_DICT[self.raw['test'].PatientSex])

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

    def tearDown(self):
        self.delete_test_file_copies_and_clean_up()

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

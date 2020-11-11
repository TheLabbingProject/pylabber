import pandas as pd

from datetime import date, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from research.models.choices import DominantHand, Sex, Gender
from ..factories import SubjectFactory


class SubjectModelTestCase(TestCase):
    def setUp(self):
        self.test_subject = SubjectFactory()
        self.test_subject.save()

        df = pd.read_excel(
            settings.RAW_SUBJECT_TABLE_PATH,
            sheet_name="Subjects",
            header=[0, 1],
            index_col=0,
        )

        subject_details = {
            ("Anonymized", "Patient ID"): "ABC123",
            ("Anonymized", "First Name"): "Noam",
            ("Anonymized", "Last Name"): "Aharony",
            ("Raw", "Patient ID"): "11111",
            ("Raw", "First Name"): "Name",
            ("Raw", "Last Name"): "Last",
        }

        for item in subject_details:
            df[item].iloc[0] = subject_details[item]

    def test_not_future_birthdate_validator(self):
        self.test_subject.date_of_birth = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.test_subject.full_clean()

    def test_null_char_field(self):
        subject_one = SubjectFactory(id_number=None)
        subject_one.save()
        subject_two = SubjectFactory(id_number=None)
        subject_two.save()
        self.assertIsNone(subject_one.id_number)
        self.assertIsNone(subject_two.id_number)

    def test_dominant_hand_choices(self):
        for choice in DominantHand:
            self.test_subject.dominant_hand = choice.name
            try:
                self.test_subject.full_clean()
            except ValidationError:
                self.fail(f"Failed to set dominant hand to {choice.value}")

    def test_invalid_dominant_hand_choice(self):
        self.test_subject.dominant_hand = "Right"
        with self.assertRaises(ValidationError):
            self.test_subject.full_clean()

    def test_sex_choices(self):
        for choice in Sex:
            self.test_subject.sex = choice.name
            try:
                self.test_subject.full_clean()
            except ValidationError:
                self.fail(f"Failed to set sex to {choice.value}")

    def test_invalid_sex_choice(self):
        self.test_subject.sex = "Z"
        with self.assertRaises(ValidationError):
            self.test_subject.full_clean()

    def test_gender_choices(self):
        for choice in Gender:
            self.test_subject.gender = choice.name
            try:
                self.test_subject.full_clean()
            except ValidationError:
                self.fail(f"Failed to set gender to {choice.value}")

    def test_invalid_gender_choice(self):
        self.test_subject.gender = "Z"
        with self.assertRaises(ValidationError):
            self.test_subject.full_clean()

    def test_get_full_name(self):
        s = self.test_subject
        expected = f"{s.first_name} {s.last_name}"
        self.assertEqual(self.test_subject.get_full_name(), expected)

    def test_str(self):
        subject_id = self.test_subject.id
        expected = f"Subject #{subject_id}"
        self.assertEqual(str(self.test_subject), expected)

    def test_get_personal_information(self):
        # @TODO: Finish the personal information test.
        # result = self.test_subject.get_personal_information()
        # result = result[[item for item in ]]

        # excpected = {
        #     ("Anonymized", "Patient ID"): "ABC123",
        #     ("Anonymized", "First Name"): "Noam",
        #     ("Anonymized", "Last Name"): "Aharony",
        #     ("Raw", "Patient ID"): "11111",
        #     ("Raw", "First Name"): "Name",
        #     ("Raw", "Last Name"): "Last",
        # }
        pass

    def test_get_raw_information(self):
        pass

    def test_get_questionnaire_data(self):
        pass

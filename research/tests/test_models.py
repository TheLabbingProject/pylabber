from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from .factories import StudyFactory, SubjectFactory
from ..models.choices import DominantHand, Sex, Gender


class SubjectModelTestCase(TestCase):
    def setUp(self):
        self.test_subject = SubjectFactory()
        self.test_subject.save()

    def test_not_future_birthdate_validator(self):
        self.test_subject.date_of_birth = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.test_subject.full_clean()

    def test_only_digits_validator(self):
        self.test_subject.id_number = "a"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "234234d23"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "23.234423"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "1/1234423"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "11123442+"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "111*34423"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "1117^4423"
        self.assertRaises(ValidationError, self.test_subject.full_clean)
        self.test_subject.id_number = "111034-33"
        self.assertRaises(ValidationError, self.test_subject.full_clean)

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
        self.test_subject.dominant_hand = "R"
        self.assertRaises(ValidationError, self.test_subject.full_clean())

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


class StudyModelTestCase(TestCase):
    def setUp(self):
        self.test_study = StudyFactory()
        self.test_study.save()

    def add_subject(self, study, exception_msg="Failed to add subject to study!"):
        subject = SubjectFactory()
        subject.save()
        try:
            study.subjects.add(subject)
        except Exception:
            self.fail(exception_msg)

    def test_add_subjects_to_study(self):
        self.add_subject(self.test_study)
        self.add_subject(
            self.test_study, "Failed to add more than one subject to study!"
        )

    def test_str(self):
        self.assertEqual(str(self.test_study), self.test_study.title)

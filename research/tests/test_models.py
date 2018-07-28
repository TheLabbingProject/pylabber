from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from research.models import Study, Subject
from research.models.choices import DominantHand, Sex, Gender

TEST_STUDY_DICT = {
    'name': 'Test Study',
    'description': 'A test study',
}

TEST_SUBJECT_DICT = {
    'first_name': 'Test',
    'last_name': 'Subject',
    'email': 'test@subject.com',
    'date_of_birth': date(1900, 1, 1),
    'id_number': '012345678',
    'phone_number': '0544123456',
    'dominant_hand': 'RIGHT',
    'sex': 'MALE',
    'gender': 'CIS',
}


class StudyModelTestCase(TestCase):
    def setUp(self):
        Study.objects.create(**TEST_STUDY_DICT)

    def get_test_study(self):
        return Study.objects.get(id=1)

    def test_setting_study_attributes(self):
        study = self.get_test_study()
        for key, value in TEST_STUDY_DICT.items():
            self.assertEqual(getattr(study, key), value)

    def test_add_subjects_to_study(self):
        study = self.get_test_study()
        # Add first subject to study
        subject = Subject.objects.create()
        try:
            study.subjects.add(subject)
        except Exception:
            self.fail('Failed to add subject to study!')
        # Add second subject to study
        another_subject = Subject.objects.create()
        try:
            study.subjects.add(another_subject)
        except Exception:
            self.fail('Failed to add more than one subject to study!')

    def test_str(self):
        study = self.get_test_study()
        expected_str = TEST_STUDY_DICT['name']
        self.assertEqual(str(study), expected_str)


class SubjectModelTestCase(TestCase):
    def setUp(self):
        Subject.objects.create(**TEST_SUBJECT_DICT)

    def get_test_subject(self):
        return Subject.objects.get(id=1)

    def test_setting_subject_attributes(self):
        subject = self.get_test_subject()
        for key, value in TEST_SUBJECT_DICT.items():
            self.assertEqual(getattr(subject, key), value)

    def test_not_future_birthdate_validator(self):
        subject = self.get_test_subject()
        subject.date_of_birth = date.today() + timedelta(days=1)
        self.assertRaises(ValidationError, subject.full_clean)

    def test_only_digits_validator(self):
        subject = self.get_test_subject()
        subject.id_number = 'a'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '234234d23'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '23.234423'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '1/1234423'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '11123442+'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '111*34423'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '1117^4423'
        self.assertRaises(ValidationError, subject.full_clean)
        subject.id_number = '111034-33'
        self.assertRaises(ValidationError, subject.full_clean)

    def test_null_char_field(self):
        subject_one = Subject.objects.create()
        subject_two = Subject.objects.create()
        self.assertEqual(subject_one.id_number, None)
        self.assertEqual(subject_two.id_number, None)

    def test_dominant_hand_choices(self):
        subject = self.get_test_subject()
        for choice in DominantHand:
            subject.dominant_hand = choice.name
            try:
                subject.full_clean()
            except ValidationError:
                self.fail(f'Failed to set dominant hand to {choice.value}')

    def test_invalid_dominant_hand_choice(self):
        subject = self.get_test_subject()
        subject.dominant_hand = 'R'
        self.assertRaises(ValidationError, subject.full_clean)

    def test_sex_choices(self):
        subject = self.get_test_subject()
        for choice in Sex:
            subject.sex = choice.name
            try:
                subject.full_clean()
            except ValidationError:
                self.fail(f'Failed to set sex to {choice.value}')

    def test_invalid_sex_choice(self):
        subject = self.get_test_subject()
        subject.sex = 'Z'
        self.assertRaises(ValidationError, subject.full_clean)

    def test_gender_choices(self):
        subject = self.get_test_subject()
        for choice in Gender:
            subject.gender = choice.name
            try:
                subject.full_clean()
            except ValidationError:
                self.fail(f'Failed to set gender to {choice.value}')

    def test_invalid_gender_choice(self):
        subject = self.get_test_subject()
        subject.gender = 'Z'
        self.assertRaises(ValidationError, subject.full_clean)

    def test_get_full_name(self):
        subject = self.get_test_subject()
        self.assertEqual(subject.get_full_name(), 'Test Subject')

    def test_str_if_both_names(self):
        subject = self.get_test_subject()
        self.assertEqual(str(subject), 'SuTe')

    def test_str_if_id_number_but_no_names(self):
        id_number = '999999999'
        subject = Subject.objects.create(
            first_name='Test', id_number=id_number)
        self.assertEqual(str(subject), id_number)

    def test_str_if_no_id_number_and_no_names(self):
        subject = Subject.objects.create()
        self.assertEqual(str(subject), f'Subject #{subject.id}')


# class StudyListViewTest(TestCase):
#     def setUp(self):
#         Study.objects.create(**TEST_STUDY_DICT)

#     def test_view_url_exists_at_proper_location(self):
#         resp = self.client.get('research/studies/')
#         self.assertEqual(resp.status_code, 200)

#     def test_view_url_by_name(self):
#         resp = self.client.get(reverse('study_list'))
#         self.assertEqual(resp.status_code, 200)

#     def test_view_uses_correct_template(self):
#         resp = self.client.get(reverse('study_list'))
#         self.assertTemplateUsed(resp, 'studies/study_list.html')

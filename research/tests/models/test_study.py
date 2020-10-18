from django.test import TestCase
from ..factories import StudyFactory, SubjectFactory


class StudyModelTestCase(TestCase):
    def setUp(self):
        self.test_study = StudyFactory()
        self.test_study.save()

    def add_subject(
        self, study, exception_msg="Failed to add subject to study!"
    ):
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

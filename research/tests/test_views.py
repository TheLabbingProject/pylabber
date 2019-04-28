# # from accounts.tests.factories import UserFactory
# from accounts.tests.utils import LoggedInTestCase
# from django.test import TestCase
# from django.urls import reverse
# from .factories import StudyFactory, SubjectFactory


# class LoggedOutStudyViewTestCase(TestCase):
#     def setUp(self):
#         self.test_study = StudyFactory()
#         self.test_study.save()

#     def test_study_list_redirects_to_login(self):
#         url = reverse("research:study_list")
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_study_detail_redirects_to_login(self):
#         url = self.test_study.get_absolute_url()
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_study_update_redirects_to_login(self):
#         url = self.test_study.get_absolute_url() + "edit/"
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_study_delete_redirects_to_login(self):
#         url = self.test_study.get_absolute_url() + "delete/"
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_study_create_redirects_to_login(self):
#         url = reverse("research:study_create")
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")


# class LoggedInStudyViewTestCase(LoggedInTestCase):
#     def setUp(self):
#         self.test_study = StudyFactory()
#         self.test_study.save()
#         super(LoggedInStudyViewTestCase, self).setUp()

#     def test_list_view(self):
#         response = self.client.get(reverse("study_list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/studies/study_list.html")

#     def test_detail_view(self):
#         url = self.test_study.get_absolute_url()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/studies/study_detail.html")

#     def test_update_view(self):
#         url = self.test_study.get_absolute_url() + "edit/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/studies/study_update.html")

#     def test_delete_view(self):
#         url = self.test_study.get_absolute_url() + "delete/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/studies/study_delete.html")

#     def test_create_view(self):
#         url = reverse("research:study_create")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/studies/study_create.html")


# class LoggedOutSubjectViewTestCase(TestCase):
#     def setUp(self):
#         self.test_subject = SubjectFactory()
#         self.test_subject.save()

#     def test_subject_list_redirects_to_login(self):
#         url = reverse("subject_list")
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_subject_detail_redirects_to_login(self):
#         url = self.test_subject.get_absolute_url()
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_subject_update_redirects_to_login(self):
#         url = self.test_subject.get_absolute_url() + "edit/"
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_subject_delete_redirects_to_login(self):
#         url = self.test_subject.get_absolute_url() + "delete/"
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")

#     def test_subject_create_redirects_to_login(self):
#         url = reverse("subject_create")
#         response = self.client.get(url, follow=True)
#         self.assertRedirects(response, f"/accounts/login/?next={url}")


# class LoggedInSubjectViewTestCase(LoggedInTestCase):
#     def setUp(self):
#         self.test_subject = SubjectFactory()
#         self.test_subject.save()
#         super(LoggedInSubjectViewTestCase, self).setUp()

#     def test_list_view(self):
#         response = self.client.get(reverse("subject_list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/subjects/subject_list.html")

#     def test_detail_view(self):
#         url = self.test_subject.get_absolute_url()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/subjects/subject_detail.html")

#     def test_update_view(self):
#         url = self.test_subject.get_absolute_url() + "edit/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/subjects/subject_update.html")

#     def test_delete_view(self):
#         url = self.test_subject.get_absolute_url() + "delete/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/subjects/subject_delete.html")

#     def test_create_view(self):
#         url = reverse("subject_create")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "research/subjects/subject_create.html")

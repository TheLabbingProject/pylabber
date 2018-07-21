from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from .mixins import StudyListMixin
from .models import Subject, Study


class StudyListView(LoginRequiredMixin, StudyListMixin, ListView):
    model = Study
    template_name = 'studies.html'


class StudyCreateView(LoginRequiredMixin, StudyListMixin, CreateView):
    model = Study
    template_name = 'studies/study_create.html'
    fields = [
        'name',
        'description',
        'collaborators',
    ]


class StudyDetailView(LoginRequiredMixin, StudyListMixin, DetailView):
    model = Study
    template_name = 'studies/study_detail.html'


class StudyUpdateView(LoginRequiredMixin, StudyListMixin, UpdateView):
    model = Study
    fields = [
        'name',
        'description',
        'collaborators',
    ]
    template_name = 'studies/study_update.html'


class StudyDeleteView(LoginRequiredMixin, StudyListMixin, DeleteView):
    model = Study
    template_name = 'studies/study_delete.html'
    success_url = reverse_lazy('study_list')


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'subjects/subject_detail.html'


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'sex',
        'date_of_birth',
        'dominant_hand',
    ]
    template_name = 'subjects/subject_update.html'


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subjects/subject_delete.html'
    success_url = reverse_lazy('subject_list')


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    template_name = 'subjects/subject_create.html'
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'sex',
        'date_of_birth',
        'dominant_hand',
    ]

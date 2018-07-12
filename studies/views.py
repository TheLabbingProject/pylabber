from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models


class StudyListView(LoginRequiredMixin, ListView):
    model = models.Study
    template_name = 'study_list.html'


class StudyDetailView(LoginRequiredMixin, DetailView):
    model = models.Study
    template_name = 'study_detail.html'


class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Study
    fields = [
        'name',
        'description',
        'collaborators',
    ]
    template_name = 'study_edit.html'


class StudyDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Study
    template_name = 'study_delete.html'
    success_url = reverse_lazy('study_list')


class StudyCreateView(LoginRequiredMixin, CreateView):
    model = models.Study
    template_name = 'study_new.html'
    fields = ['name', 'description', 'collaborators']

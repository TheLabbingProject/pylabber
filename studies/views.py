from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models


class StudyListView(LoginRequiredMixin, ListView):
    model = models.Study
    template_name = 'studies.html'


class StudyDetailView(LoginRequiredMixin, DetailView):
    model = models.Study
    template_name = 'study_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudyDetailView, self).get_context_data(**kwargs)
        context['object_list'] = models.Study.objects.all()
        return context


class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Study
    fields = [
        'name',
        'description',
        'collaborators',
    ]
    template_name = 'study_edit.html'

    def get_context_data(self, **kwargs):
        context = super(StudyUpdateView, self).get_context_data(**kwargs)
        context['object_list'] = models.Study.objects.all()
        return context


class StudyDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Study
    template_name = 'study_delete.html'
    success_url = reverse_lazy('study_list')

    def get_context_data(self, **kwargs):
        context = super(StudyDeleteView, self).get_context_data(**kwargs)
        context['object_list'] = models.Study.objects.all()
        return context


class StudyCreateView(LoginRequiredMixin, CreateView):
    model = models.Study
    template_name = 'study_new.html'
    fields = ['name', 'description', 'collaborators']

    def get_context_data(self, **kwargs):
        context = super(StudyCreateView, self).get_context_data(**kwargs)
        context['object_list'] = models.Study.objects.all()
        return context

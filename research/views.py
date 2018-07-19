from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Study


class StudyListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studies'] = Study.objects.all()
        return context


class StudyListView(LoginRequiredMixin, StudyListMixin, ListView):
    model = Study
    template_name = 'studies.html'


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
    template_name = 'studies/study_edit.html'


class StudyDeleteView(LoginRequiredMixin, StudyListMixin, DeleteView):
    model = Study
    template_name = 'studies/study_delete.html'
    success_url = reverse_lazy('study_list')


class StudyCreateView(LoginRequiredMixin, StudyListMixin, CreateView):
    model = Study
    template_name = 'studies/study_new.html'
    fields = ['name', 'description', 'collaborators']

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .filters import SubjectListFilter
from .forms import SubjectListFormHelper
from .mixins import StudyListMixin
from .models import Subject, Study
from .tables import SubjectTable
from .utils import FilteredTableMixin
if 'questionnaires' in settings.INSTALLED_APPS:
    from questionnaires.mixins import QuestionnaireListMixin


class StudyListView(LoginRequiredMixin, ListView):
    model = Study
    template_name = 'research/studies/study_list.html'
    context_object_name = 'studies'


class StudyCreateView(LoginRequiredMixin, StudyListMixin, CreateView):
    model = Study
    template_name = 'research/studies/study_create.html'
    fields = [
        'name',
        'description',
        'collaborators',
    ]


class StudyDetailView(LoginRequiredMixin, StudyListMixin, DetailView):
    model = Study
    template_name = 'research/studies/study_detail.html'


class StudyUpdateView(LoginRequiredMixin, StudyListMixin, UpdateView):
    model = Study
    fields = [
        'name',
        'description',
        'collaborators',
    ]
    template_name = 'research/studies/study_update.html'


class StudyDeleteView(LoginRequiredMixin, StudyListMixin, DeleteView):
    model = Study
    template_name = 'research/studies/study_delete.html'
    success_url = reverse_lazy('study_list')


class SubjectListView(LoginRequiredMixin, FilteredTableMixin):
    model = Subject
    table_class = SubjectTable
    template_name = 'research/subjects/subject_list.html'
    paginate_by = 50
    ordering = ['-id']
    filterset_class = SubjectListFilter
    formhelper_class = SubjectListFormHelper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.get_queryset()
        table = self.table_class(search_query)
        context['table'] = table
        return context


class SubjectDetailView(SubjectListView):
    model = Subject
    template_name = 'research/subjects/subject_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(id=self.kwargs.get('pk'))
        context['subject'] = subject
        return context


class SubjectUpdateView(SubjectListView, UpdateView):
    model = Subject
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'sex',
        'gender',
        'date_of_birth',
        'dominant_hand',
    ]
    template_name = 'research/subjects/subject_update.html'

    def get_context_data(self, **kwargs):
        subject = Subject.objects.get(id=self.kwargs['pk'])
        self.object = subject
        context = super().get_context_data(**kwargs)
        context['subject'] = subject
        return context


class SubjectDeleteView(SubjectListView, DeleteView):
    model = Subject
    template_name = 'research/subjects/subject_delete.html'
    success_url = reverse_lazy('subject_list')

    def get_context_data(self, **kwargs):
        subject = Subject.objects.get(id=self.kwargs['pk'])
        self.object = subject
        context = super().get_context_data(**kwargs)
        context['subject'] = subject
        return context


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    template_name = 'research/subjects/subject_create.html'
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'sex',
        'date_of_birth',
        'dominant_hand',
    ]


class DataSummaryView(LoginRequiredMixin, QuestionnaireListMixin,
                      TemplateView):
    template_name = 'research/data/data_nav.html'

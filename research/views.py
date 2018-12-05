from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django_dicom.models import Instance
from django_tables2 import RequestConfig
from django_smb.models import RemotePath
from django_smb.views import RemoteLocationCreateView, RemoteLocationListView
from pylabber.utils import FilteredTableMixin
from .filters import SubjectListFilter
from .forms import SubjectListFormHelper
from .mixins import StudyListMixin
from .models import Subject, Study
from .tables import SubjectTable


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
    success_url = reverse_lazy('research:study_list')


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
    success_url = reverse_lazy('research:study_list')


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
        RequestConfig(self.request).configure(table)
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
        'id_number',
        'first_name',
        'last_name',
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
    success_url = reverse_lazy('research:subject_list')

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
        'id_number',
        'first_name',
        'last_name',
        'sex',
        'gender',
        'date_of_birth',
        'dominant_hand',
    ]


class DataSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'research/data/data_nav.html'


class DataSourcesSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'research/data_sources/data_sources_nav.html'


CREATE_SMB = 'research/data_sources/smb/create_location.html'
RemoteLocationCreateView.template_name = CREATE_SMB

LIST_SMB_FILES = 'research/data_sources/smb/list_files.html'
RemoteLocationListView.template_name = LIST_SMB_FILES


def import_dcms_from_node(node: RemotePath):
    try:
        for descendant in node.get_descendants(include_self=True):
            if descendant.name.endswith('.dcm') and not descendant.is_imported:
                f = descendant.get_file()
                Instance.objects.from_dcm(f)
                descendant.is_imported = True
                descendant.save()
        return True
    except Exception as e:
        print(e)
        return False


def import_node(request):
    if request.method == 'GET':
        request_path = request.get_full_path()
        path_id = request_path.split('=')[-1]
        node = RemotePath.objects.get(id=path_id)
        result = import_dcms_from_node(node)
        if result:
            return HttpResponse(node.id)
        return HttpResponse(f'Failure')
    else:
        return HttpResponse('Request method must be GET!')

import numpy as np

from bokeh.embed import server_session
from bokeh.util import session_id
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView
from django_tables2 import RequestConfig
from pylabber.utils import FilteredTableMixin
from .filters import SMBFileListFilter
from .forms import CreateInstancesForm, SMBDirectoryForm, SMBFileListFormHelper
from .models import (
    Instance,
    Series,
    Study,
    Patient,
    SMBDirectory,
    SMBFile,
)
from .tables import SMBFileTable


class InstanceListView(LoginRequiredMixin, ListView):
    model = Instance
    template_name = 'dicom/instances/instance_list.html'


class InstanceDetailView(LoginRequiredMixin, DetailView):
    model = Instance
    template_name = 'dicom/instances/instance_detail.html'


class InstancesCreateView(LoginRequiredMixin, FormView):
    form_class = CreateInstancesForm
    template_name = 'dicom/instances/instances_create.html'
    success_url = reverse_lazy('instance_list')
    temp_file_name = 'tmp.dcm'
    temp_zip_name = 'tmp.zip'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('dcm_files')
            for file in files:
                if file.name.endswith('.dcm'):
                    Instance.objects.from_dcm(file)
                elif file.name.endswith('.zip'):
                    Instance.objects.from_zip(file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SeriesDetailView(LoginRequiredMixin, DetailView):
    model = Series
    template_name = 'dicom/series/series_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SeriesDetailView, self).get_context_data(**kwargs)
        bokeh_server_url = 'http://127.0.0.1:5006/app'
        data = context['object'].get_data()
        np.save('/home/zvi/Projects/series_viewer/data', data)
        server_script = server_session(
            None,
            session_id=session_id.generate_session_id(),
            url=bokeh_server_url,
        )
        extra = {
            'server_script': server_script,
        }
        context.update(extra)
        return context


class SeriesListView(LoginRequiredMixin, ListView):
    model = Series
    template_name = 'dicom/series/series_list.html'


class StudyDetailView(LoginRequiredMixin, DetailView):
    model = Study
    template_name = 'dicom/studies/study_detail.html'


class StudyListView(LoginRequiredMixin, ListView):
    model = Study
    template_name = 'dicom/studies/study_list.html'


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'dicom/patients/patient_detail.html'


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'dicom/patients/patient_list.html'


def update_smb_location(request, pk: int):
    smb = get_object_or_404(SMBDirectory, pk=pk)
    SMBFile.objects.update_smb(smb)
    return redirect(SMBFile)


class SMBDirectoryListView(LoginRequiredMixin, ListView):
    model = SMBDirectory
    template_name = 'dicom/data_sources/smb/smb_directory_list.html'


class SMBFileListView(LoginRequiredMixin, FilteredTableMixin):
    model = SMBFile
    table_class = SMBFileTable
    template_name = 'dicom/data_sources/smb/smb_file_list.html'
    paginate_by = 50
    ordering = ['-id']
    filterset_class = SMBFileListFilter
    formhelper_class = SMBFileListFormHelper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.get_queryset()
        table = self.table_class(search_query)
        RequestConfig(self.request).configure(table)
        context['table'] = table
        return context


class SMBDirectoryCreateView(LoginRequiredMixin, CreateView):
    form_class = SMBDirectoryForm
    template_name = 'dicom/data_sources/smb/smb_directory_create.html'
    success_url = reverse_lazy('smb_directory_list')

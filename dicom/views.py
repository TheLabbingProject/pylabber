from bokeh.embed import server_session
from bokeh.util import session_id
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .forms import CreateInstancesForm
from .models import Instance, Series, Study, Patient


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


@login_required
def series_view(request):
    absolute_url = request.build_absolute_uri(location="/")
    bokeh_server_url = f'{absolute_url}bokehproxy/series_plot'
    server_script = server_session(
        None,
        session_id=session_id.generate_session_id(),
        url=bokeh_server_url)
    context = {
        'graph_name': 'MRI Series Viewer',
        'server_script': server_script,
    }
    return render(request, 'series/bokeh_server.html', context)


class SeriesDetailView(LoginRequiredMixin, DetailView):
    model = Series
    template_name = 'dicom/series/series_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(SeriesDetailView, self).get_context_data(**kwargs)
    #     absolute_url = self.request.build_absolute_uri(location="/")
    #     bokeh_server_url = f'{absolute_url}bokehproxy/series_plot'
    #     server_script = server_session(
    #         None,
    #         session_id=session_id.generate_session_id(),
    #         url=bokeh_server_url)
    #     extra = {
    #         'graph_name': 'MRI Series Viewer',
    #         'server_script': server_script,
    #     }
    #     return context.update(extra)


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

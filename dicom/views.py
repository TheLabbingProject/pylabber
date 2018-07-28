import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import CreateInstancesForm
from .models import Instance


class InstanceListView(LoginRequiredMixin, ListView):
    model = Instance
    template_name = 'instances/instance_list.html'


class InstanceDetailView(LoginRequiredMixin, DetailView):
    model = Instance
    template_name = 'instances/instance_detail.html'


class InstancesCreateView(LoginRequiredMixin, FormView):
    form_class = CreateInstancesForm
    template_name = 'instances/instances_create.html'
    success_url = reverse_lazy('instance_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('dcm_files')
            for f in files:
                temp_path = default_storage.save('tmp.dcm',
                                                 ContentFile(f.read()))
                temp_path = os.path.join(settings.MEDIA_ROOT, temp_path)
                instance = Instance()
                instance.file = 'tmp.dcm'
                instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

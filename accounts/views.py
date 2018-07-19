from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from . import models


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User
    template_name = 'user_detail.html'
    context_object_name = 'object'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Profile
    template_name = 'profile_update.html'
    fields = [
        'date_of_birth',
        'institute',
        'bio',
    ]
    # TODO: Fix permissions so that other users can't access profile edit page

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from . import models


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User
    template_name = 'user_detail.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Profile
    template_name = 'profile_edit.html'
    fields = [
        'date_of_birth',
        'institute',
        'bio',
    ]

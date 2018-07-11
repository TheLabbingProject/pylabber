from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView, DetailView

from .forms import LoginForm
from . import models


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        form_data = form.cleaned_data

        user = authenticate(
            email=form_data['email'], password=form_data['password'])

        if not user:
            error_message = 'Invalid e-mail / password combination'
            messages.error(self.request, _(error_message))
            context_data = self.get_context_data(
                request=self.request, form=form)
            return self.render_to_response(context_data, status=401)

        return super().form_valid(form)


class DetailsView(LoginRequiredMixin, DetailView):
    model = models.User
    template_name = 'accounts/details.html'
    login_url = 'login'

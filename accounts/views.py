from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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

    def dispatch(self, request, *args, **kwargs):
        """
        Restricts access to the logged-in user.

        :param request: HTTP request method.
        :type request: django.http.HttpRequest
        :return: Profile update page or unauthorized.
        :rtype: django.http.HttpRespone
        """

        user = self.get_object()
        if user.id != self.request.user.id:
            raise PermissionDenied
        return super(ProfileUpdateView, self).dispatch(request, *args,
                                                       **kwargs)

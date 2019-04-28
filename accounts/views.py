from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from accounts.models import User, Profile


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "object"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile_update.html"
    fields = ["date_of_birth", "institute", "bio"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Restricts access to the logged-in user.
        
        Parameters
        ----------
        request : HttpRequest
            An HTTP request to the view.
        
        Raises
        ------
        PermissionDenied
            If the requested ProfileUpdateView does not belong to the requesting user.

        Returns
        -------
        HttpResponse
            The requested view.
        """

        user = self.get_object()
        if user.id != self.request.user.id:
            raise PermissionDenied
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

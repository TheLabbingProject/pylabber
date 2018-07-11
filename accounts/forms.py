from django import forms
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': _('E-mail address')}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))

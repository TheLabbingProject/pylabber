from django import forms

from research.models import Subject


class CreateInstancesForm(forms.Form):
    dcm_files = forms.FileField(
        label='DICOM files',
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    subject = forms.ModelChoiceField(Subject.objects)

from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Fieldset
from django import forms
from .models.smb_directory import SMBDirectory


class CreateInstancesForm(forms.Form):
    dcm_files = forms.FileField(
        label='DICOM files',
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SMBDirectoryForm(forms.ModelForm):
    class Meta:
        model = SMBDirectory
        fields = [
            'name',
            'server_name',
            'share_name',
            'user_id',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }


class SMBFileListFormHelper(FormHelper):
    form_id = 'smb-file-search-form'
    # form_class = "smb-file-search-form"
    field_class = 'mb-2'
    label_class = 'mr-2 ml-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
        Fieldset(
            '<i class="fa fa-search"></i> Search SMB File Records',
            Div(
                'id',
                'path',
                'source',
                'is_archived',
                css_class='row',
            ),
            css_class='row',
        ),
        Div(
            FormActions(
                StrictButton(
                    'Search',
                    type='submit',
                    css_class='btn btn-info',
                    style='margin-top: 40px; margin-left: 500px;',
                )),
            css_class='row',
        ),
    )

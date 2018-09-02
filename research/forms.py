from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML


class SubjectListFormHelper(FormHelper):
    form_id = 'subject-search-form'
    # form_class = "subject-search-form"
    field_class = 'mb-2'
    label_class = 'mr-2 ml-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
        Fieldset(
            '<i class="fa fa-search"></i> Search Subject Records',
            Div(
                'id',
                'id_number',
                css_class='row',
            ),
            Div(
                'first_name',
                'last_name',
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
                    style='margin-top: 20px; margin-left: 40px;',
                )),
            css_class='row',
        ),
        HTML('<hr>'),
    )

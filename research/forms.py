from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML


class SubjectListFormHelper(FormHelper):
    form_id = 'subject-search-form'
    # form_class = "form-search"
    # field_class = 'col-xs-3'
    # label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
        Div(
            Div(
                Fieldset(
                    '<i class="fa fa-search"></i> Search Subject Records'),
                css_class='row',
            ),
            Div(
                Div(
                    Field('id'),
                    css_class='col-2',
                ),
                Div(
                    Field('id_number'),
                    css_class='col-2',
                ),
                Div(
                    Field('first_name'),
                    css_class='col-2',
                ),
                Div(
                    Field('last_name'),
                    css_class='col-2',
                ),
                Div(
                    Field('sex'),
                    css_class='col-2',
                ),
                Div(
                    Field('gender'),
                    css_class='col-2',
                ),
                css_class='row',
            ),
            Div(
                Div(
                    Field(
                        'date_of_birth',
                        css_class='datepicker',
                    ),
                    css_class='col-2',
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
            css_class='container-fluid',
        ))

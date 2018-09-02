from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML


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
        # Div(
        #     Div(
        #         Fieldset(
        #             '<i class="fa fa-search"></i> Search Subject Records'),
        #         css_class='row',
        #     ),
        #     Div(
        #         Div(
        #             Field(
        #                 'id',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 col',
        #         ),
        #         Div(
        #             Field(
        #                 'id_number',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 ml-4 col',
        #         ),
        #         Div(
        #             Field(
        #                 'first_name',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 ml-4 col',
        #         ),
        #         Div(
        #             Field(
        #                 'last_name',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 ml-4 col',
        #         ),
        #         css_class='row',
        #     ),
        #     Div(
        #         Div(
        #             Field(
        #                 'sex',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 ml-4 col',
        #         ),
        #         Div(
        #             Field(
        #                 'gender',
        #                 css_class='ml-2',
        #             ),
        #             css_class='mb-2 ml-4 col',
        #         ),
        #         css_class='row',
        #     ),
        #     Div(
        #         Div(
        #             Field(
        #                 'date_of_birth',
        #                 css_class='datepicker',
        #                 placeholder='dd/mm/yyyy',
        #             ),
        #             css_class='mb-2',
        #         ),
        #         Div(
        #             Field(
        #                 'date_of_birth__gt',
        #                 placeholder='yyyy',
        #             ),
        #             css_class='mb-2',
        #         ),
        #         Div(
        #             Field(
        #                 'date_of_birth__lt',
        #                 placeholder='yyyy',
        #             ),
        #             css_class='mb-2',
        #             placeholder='yyyy',
        #         ),
        #         css_class='row',
        #     ),
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
        # css_class='container-fluid',
    )

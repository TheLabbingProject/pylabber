from django.core.validators import RegexValidator

digits_only = RegexValidator(
    '^\d+$',
    message='Digits only!',
    code='invalid_patient_uid',
)

digits_and_dots_only = RegexValidator(
    '^\d+(\.\d+)*$',
    message='Digits and dots only!',
    code='invalid_uid',
)

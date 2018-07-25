from django.core.validators import RegexValidator

digits_only = RegexValidator(
    '^\d+$',
    message='Digits only!',
    code='invalid_number',
)
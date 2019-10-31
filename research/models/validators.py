"""
`Validators <https://docs.djangoproject.com/en/2.2/ref/validators/>`_
for django fields within the :mod:`research.models` module.

"""

from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from research.models.choices import CustomAttributeTypes

digits_only = RegexValidator("^\d+$", message="Digits only!", code="invalid_number")


def not_future(value):
    if value > date.today():
        raise ValidationError("Date cannot be in the future.")


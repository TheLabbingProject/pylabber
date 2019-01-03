from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

digits_only = RegexValidator("^\d+$", message="Digits only!", code="invalid_number")


def not_future(value):
    if value > date.today():
        raise ValidationError("Date cannot be in the future.")

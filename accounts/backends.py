from django.contrib.auth import get_user_model
from django.core.validators import ValidationError, validate_email

User = get_user_model()


class EmailModelBackend:
    """
    This is a ModelBacked that allows authentication with an email address.
    """

    def authenticate(self, request, email=None, password=None):
        try:
            validate_email(email)
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except (ValidationError, User.DoesNotExist):
            return None

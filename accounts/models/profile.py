from accounts.models.choices import Title
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """
    A user profile, associated to each user using a OneToOne relationship and
    created automatically usings signals.
    For more information see `this example <https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html>`_.

    """

    # One-to-one relationship with the user model
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )

    # Academic or any other kind of title
    title = models.CharField(
        max_length=20, choices=Title.choices(), default="", blank=True, null=True
    )

    image = models.ImageField(upload_to="images/profiles", blank=True)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.get_full_name()

    def get_absolute_url(self) -> str:
        return reverse("accounts:user_detail", args=[str(self.user.id)])

    def get_full_name(self) -> str:
        """
        Returns the full name of the user, including a title if any.

        Returns
        -------
        str
            User's full name.
        """

        if self.title:
            title = Title[self.title].value
            return f"{self.user.get_full_name()}, {title}"
        return self.user.get_full_name()

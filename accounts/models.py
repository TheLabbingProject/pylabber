from accounts.choices import Title, Position
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Set the order by which to present lab members (users) in the home page
# using a custom SQL statement.
TITLE_ORDERING_SQL = "case when position='PI' then 1 when position='MAN' then 2 when position='PHD' then 3 when position='MSC' then 4 end"


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField(upload_to="images/profiles", blank=True)
    title = models.CharField(
        max_length=20, choices=Title.choices(), default="", blank=True, null=True
    )
    position = models.CharField(
        max_length=20, choices=Position.choices(), default="", blank=True, null=True
    )
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

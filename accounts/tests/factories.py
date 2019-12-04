import datetime
import factory

from accounts.models import Profile
from accounts.models.choices import Title, Role
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from random import randint

TEST_PASSWORD = "Aa123456"
TITLES = [title.name for title in Title]
ROLES = [role.name for role in Role]


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ("user",)

    title = factory.Faker("random_element", elements=TITLES)
    date_of_birth = factory.Faker("date_this_century", before_today=True)
    institute = factory.Faker("company")
    # position = factory.Faker("random_element", elements=ROLES)
    bio = factory.Faker("text", max_nb_chars=500)

    # We pass in profile=None to prevent UserFactory from creating another
    # profile (this disables the RelatedFactory)
    user = factory.SubFactory("accounts.tests.factories.UserFactory", profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ("username",)
        strategy = factory.BUILD_STRATEGY

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: f"user{str(n).zfill(3)}")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", TEST_PASSWORD)

    @factory.lazy_attribute
    def date_joined(self):
        return timezone.now() - datetime.timedelta(days=randint(5, 50))

    last_login = factory.lazy_attribute(
        lambda o: o.date_joined + datetime.timedelta(days=4)
    )

    is_superuser = True
    is_staff = True
    is_active = True

    # We pass in 'user' to link the generated Profile to our just-generated
    # User. This will call ProfileFactory(user=our_new_user), thus skipping the
    # SubFactory.
    profile = factory.RelatedFactory(ProfileFactory, "user")

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

import factory

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raw_password = kwargs['password']
        kwargs['password'] = make_password(raw_password)
        user = super()._create(model_class, *args, **kwargs)
        user._password = raw_password
        return user

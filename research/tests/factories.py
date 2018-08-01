import datetime
import factory
import factory.fuzzy

from accounts.tests.factories import UserFactory
from django.utils import timezone
from random import randint
from ..models import Study, Subject, choices

DIGITS = [str(i) for i in range(10)]
DOMINANT_HAND_CHOICES = [option.name for option in choices.DominantHand]
SEX_CHOICES = [option.name for option in choices.Sex]
GENDER_CHOICES = [option.name for option in choices.Gender]


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
        strategy = factory.BUILD_STRATEGY

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_this_century', before_today=True)
    id_number = factory.fuzzy.FuzzyText(length=9, chars=DIGITS)
    phone_number = factory.fuzzy.FuzzyText(length=10, chars=DIGITS)
    dominant_hand = factory.fuzzy.FuzzyChoice(DOMINANT_HAND_CHOICES)
    sex = factory.fuzzy.FuzzyChoice(SEX_CHOICES)
    gender = factory.fuzzy.FuzzyChoice(GENDER_CHOICES)


class StudyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Study
        strategy = factory.BUILD_STRATEGY

    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=4)

    @factory.lazy_attribute
    def created_at(self):
        return timezone.now() - datetime.timedelta(days=randint(5, 50))

    updated_at = factory.lazy_attribute(
        lambda o: o.created_at + datetime.timedelta(days=4))

    subjects = factory.RelatedFactory(SubjectFactory)
    collaborators = factory.RelatedFactory(UserFactory)

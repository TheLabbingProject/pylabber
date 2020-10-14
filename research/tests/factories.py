import datetime
import factory
import factory.fuzzy

from accounts.tests.factories import UserFactory
from django.utils import timezone
from random import randint
from research.models import (
    Study,
    Subject,
    Task,
    Event,
    MeasurementDefinition,
    Procedure,
    ProcedureStep,
    choices,
)

DIGITS = [str(i) for i in range(10)]
DOMINANT_HAND_CHOICES = [option.name for option in choices.DominantHand]
SEX_CHOICES = [option.name for option in choices.Sex]
GENDER_CHOICES = [option.name for option in choices.Gender]


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
        strategy = factory.BUILD_STRATEGY

    id_number = factory.fuzzy.FuzzyText(length=9, chars=DIGITS)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_this_century", before_today=True)
    dominant_hand = factory.fuzzy.FuzzyChoice(DOMINANT_HAND_CHOICES)
    sex = factory.fuzzy.FuzzyChoice(SEX_CHOICES)
    gender = factory.fuzzy.FuzzyChoice(GENDER_CHOICES)


class StudyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Study
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("paragraph", nb_sentences=4)

    @factory.lazy_attribute
    def created(self):
        return timezone.now() - datetime.timedelta(days=randint(5, 50))

    modified = factory.lazy_attribute(
        lambda o: o.created + datetime.timedelta(days=4)
    )

    subjects = factory.RelatedFactory(SubjectFactory)
    collaborators = factory.RelatedFactory(UserFactory)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("paragraph", nb_sentences=4)


class TaskFactory(EventFactory):
    class Meta:
        model = Task
        strategy = factory.BUILD_STRATEGY


class MeasurementDefinitionFactory(EventFactory):
    class Meta:
        model = MeasurementDefinition
        strategy = factory.BUILD_STRATEGY


class ProcedureStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProcedureStep
        strategy = factory.BUILD_STRATEGY

    event = factory.SubFactory(EventFactory)
    index = factory.Faker("random_int", min=0)


class ProcedureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Procedure
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("paragraph", nb_sentences=4)

    events = factory.RelatedFactory(
        ProcedureStepFactory, factory_related_name="procedure"
    )
    index = 0


import factory
import pytz

from django.db.models.signals import pre_save
from mri.models.nifti import NIfTI
from mri.models.sequence_type import SequenceType
from mri.models.scan import Scan
from mri.models.choices import ScanningSequence, SequenceVariant
from research.tests.factories import SubjectFactory

SCANNING_SEQUENCES = [sequence.name for sequence in ScanningSequence]
SEQUENCE_VARIANTS = [variant.name for variant in SequenceVariant]


class SequenceTypeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    description = factory.Faker("text", max_nb_chars=50)
    scanning_sequence = factory.Faker(
        "words", nb=3, ext_word_list=SCANNING_SEQUENCES, unique=True
    )
    sequence_variant = factory.Faker("words", nb=2, ext_word_list=SEQUENCE_VARIANTS)

    class Meta:
        model = SequenceType


@factory.django.mute_signals(pre_save)
class ScanFactory(factory.django.DjangoModelFactory):
    time = factory.Faker("date_time_this_century", before_now=True, tzinfo=pytz.UTC)
    description = factory.Faker("sentence", nb_words=5)
    number = factory.Faker("random_int", min=0, max=300)
    echo_time = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)
    repetition_time = factory.Faker("pyfloat", positive=True, left_digits=2)
    inversion_time = factory.Faker("pyfloat", positive=True, left_digits=2)
    # spatial_resolution = factory.Faker("pylist", float, nb_elements=3)
    sequence_type = factory.SubFactory(SequenceTypeFactory)
    comments = factory.Faker("sentence", nb_words=10)
    subject = factory.SubFactory(SubjectFactory)
    _nifti = factory.SubFactory("mri.tests.factories.NIfTIFactory", parent=None)

    class Meta:
        model = Scan


class NIfTIFactory(factory.django.DjangoModelFactory):
    path = factory.Faker("file_path", depth=4, extension="nii.gz")
    is_raw = factory.Faker("boolean")
    parent = factory.SubFactory(ScanFactory)

    class Meta:
        model = NIfTI

import pydicom

from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator

digits_and_dots_only = RegexValidator(
    '^\d+(\.\d+)*$',
    message='Digits and dots only!',
    code='invalid_uid',
)


class Series(models.Model):
    id = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        validators=[digits_and_dots_only],
    )
    number = models.IntegerField(verbose_name='Series Number')
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = 'Series'


class Study(models.Model):
    id = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        validators=[digits_and_dots_only],
    )
    description = models.CharField(max_length=64)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = 'Studies'


class Patient(models.Model):
    id = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        validators=[digits_and_dots_only],
    )
    given_name = models.CharField(max_length=64, blank=True)
    family_name = models.CharField(max_length=64, blank=True)
    middle_name = models.CharField(max_length=64, blank=True)
    name_prefix = models.CharField(max_length=64, blank=True)
    name_suffix = models.CharField(max_length=64, blank=True)
    date_of_birth = models.DateField()

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
    )

    subject = models.OneToOneField(
        'research.Subject',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.id


class Instance(models.Model):
    _headers = None

    id = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        validators=[digits_and_dots_only],
    )

    path = models.CharField(
        max_length=500,
        verbose_name='File Path',
    )
    number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Instance Number',
    )
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    series = models.ForeignKey(
        Series, blank=True, null=True, on_delete=models.CASCADE)
    study = models.ForeignKey(
        Study, blank=True, null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Patient, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def read_data(self):
        return pydicom.dcmread(self.path)

    def read_headers(self):
        return pydicom.dcmread(self.path, stop_before_pixels=True)

    def parse_DA(self, value):
        return datetime.strptime(value, '%Y%m%d').date()

    def parse_TM(self, value):
        return datetime.strptime(value, '%H%M%S.%f').time()

    def get_series_dict(self):
        return {
            'id': self.headers.SeriesInstanceUID,
            'number': int(self.headers.SeriesNumber),
            'date': self.parse_DA(self.headers.SeriesDate),
            'time': self.parse_TM(self.headers.SeriesTime),
            'description': self.headers.SeriesDescription,
        }

    def create_series(self):
        return Series.objects.create(**self.get_series_dict())

    def get_series(self):
        series_uid = self.headers.SeriesInstanceUID
        series = Series.objects.filter(id=series_uid).first()
        if not series:
            series = self.create_series()
        return series

    def get_study_dict(self):
        return {
            'id': self.headers.StudyInstanceUID,
            'date': self.parse_DA(self.headers.StudyDate),
            'time': self.parse_TM(self.headers.StudyTime),
            'description': self.headers.StudyDescription,
        }

    def create_study(self):
        return Study.objects.create(**self.get_study_dict())

    def get_study(self):
        study_uid = self.headers.StudyInstanceUID
        study = Study.objects.filter(id=study_uid).first()
        if not study:
            study = self.create_study()
        return study

    def get_patient_dict(self):
        return {
            'id': self.headers.PatientID,
            'given_name': self.headers.PatientName.given_name,
            'family_name': self.headers.PatientName.family_name,
            'middle_name': self.headers.PatientName.middle_name,
            'name_prefix': self.headers.PatientName.name_prefix,
            'name_suffix': self.headers.PatientName.name_suffix,
            'date_of_birth': self.parse_DA(self.headers.PatientBirthDate),
            'sex': self.headers.PatientSex,
        }

    def create_patient(self):
        return Patient.objects.create(**self.get_patient_dict())

    def get_patient(self):
        patient_id = self.headers.PatientID
        patient = Patient.objects.filter(id=patient_id).first()
        if not patient:
            patient = self.create_patient()
        return patient

    def get_attributes_from_file(self, path: str):
        return {
            'id': self.headers.SOPInstanceUID,
            'number': int(self.headers.InstanceNumber),
            'date': self.parse_DA(self.headers.InstanceCreationDate),
            'time': self.parse_TM(self.headers.InstanceCreationTime),
            'series': self.get_series(),
            'study': self.get_study(),
            'patient': self.get_patient(),
        }

    def save(self, *args, **kwargs):
        attributes = self.get_attributes_from_file(self.path)
        for key, value in attributes.items():
            setattr(self, key, value)
        super(Instance, self).save(*args, **kwargs)

    @property
    def headers(self):
        if self._headers is None:
            self._headers = self.read_headers()
        return self._headers

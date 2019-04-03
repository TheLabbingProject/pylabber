import numpy as np
import os
import pytz

from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django_dicom.interfaces.dcm2niix import Dcm2niix
from django_nipype.models.interfaces.fsl.bet import BetConfiguration, BetRun
from django_nipype.models.interfaces.fsl.flirt import FlirtConfiguration, FlirtRun
from mri.models.managers import ScanManager
from mri.models.nifti import NIfTI
from mri.models.sequence_type import SequenceType


class Scan(models.Model):
    number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    echo_time = models.FloatField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    inversion_time = models.FloatField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    repetition_time = models.FloatField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    spatial_resolution = ArrayField(models.FloatField(blank=True, null=True), size=3)
    comments = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    dicom = models.OneToOneField(
        "django_dicom.Series", on_delete=models.PROTECT, blank=True, null=True
    )
    sequence_type = models.ForeignKey(
        "mri.SequenceType", on_delete=models.PROTECT, blank=True, null=True
    )
    _nifti = models.OneToOneField(
        "mri.NIfTI", on_delete=models.PROTECT, blank=True, null=True
    )
    subject = models.ForeignKey(
        "research.Subject", on_delete=models.PROTECT, blank=True, null=True
    )

    objects = ScanManager()

    class Meta:
        ordering = ("time",)
        verbose_name_plural = "MRI Scans"

    def update_fields_from_dicom(self) -> bool:
        if self.dicom:
            self.number = self.dicom.number
            self.time = datetime.combine(
                self.dicom.date, self.dicom.time, tzinfo=pytz.UTC
            )
            self.description = self.dicom.description
            self.echo_time = self.dicom.echo_time
            self.inversion_time = self.dicom.inversion_time
            self.repetition_time = self.dicom.repetition_time
            self.spatial_resolution = self.get_spatial_resolution_from_dicom()
            self.sequence_type = self.infer_sequence_type_from_dicom()
            return True
        else:
            raise AttributeError(f"No DICOM data associated with MRI scan {self.id}!")

    def get_spatial_resolution_from_dicom(self) -> list:
        try:
            return self.dicom.pixel_spacing + [
                self.dicom.get_series_attribute("SliceThickness")
            ]
        except TypeError:
            return []

    def infer_sequence_type_from_dicom(self) -> SequenceType:
        try:
            return SequenceType.objects.get(
                scanning_sequence=self.dicom.scanning_sequence,
                sequence_variant=self.dicom.sequence_variant,
            )
        except models.ObjectDoesNotExist:
            return None

    def get_default_nifti_dir(self):
        if self.dicom:
            return self.dicom.get_path().replace("DICOM", "NIfTI")

    def get_default_nifti_name(self):
        return str(self.id)

    def get_default_nifti_destination(self):
        directory = self.get_default_nifti_dir()
        name = self.get_default_nifti_name()
        return os.path.join(directory, name)

    def dicom_to_nifti(self, destination: str = None):
        if self.dicom:
            dcm2niix = Dcm2niix()
            destination = destination or self.get_default_nifti_destination()
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            nifti_path = dcm2niix.convert(self.dicom.get_path(), destination)
            nifti = NIfTI.objects.create(path=nifti_path, parent=self, is_raw=True)
            return nifti
        else:
            raise NotImplementedError

    def extract_brain(self, configuration: BetConfiguration = None) -> NIfTI:
        if not configuration:
            configuration = BetConfiguration.objects.get_or_create(
                mode=BetConfiguration.ROBUST
            )[0]
        bet_run = BetRun.objects.get_or_create(
            in_file=self.nifti.path, configuration=configuration, output=[BetRun.BRAIN]
        )[0]
        bet_results = bet_run.run()
        return NIfTI.objects.get_or_create(
            path=bet_results.out_file, parent=self, is_raw=False
        )[0]

    def extract_skull(self, configuration: BetConfiguration = None) -> NIfTI:
        if not configuration:
            configuration = BetConfiguration.objects.get_or_create(
                mode=BetConfiguration.ROBUST
            )[0]
        bet_run = BetRun.objects.get_or_create(
            in_file=self.nifti.path, configuration=configuration, output=[BetRun.SKULL]
        )[0]
        bet_results = bet_run.run()
        return NIfTI.objects.get_or_create(
            path=bet_results.skull, parent=self, is_raw=False
        )[0]

    def register_brain_to_mni_space(
        self, configuration: FlirtConfiguration = None
    ) -> NIfTI:
        if not configuration:
            configuration = FlirtConfiguration.objects.get_or_create()[0]
        fsl_path = os.environ["FSLDIR"]
        mni_path = os.path.join(
            fsl_path, "data", "standard", "MNI152_T1_1mm_brain.nii.gz"
        )
        flirt_run = FlirtRun.objects.get_or_create(
            in_file=self.brain.path, reference=mni_path, configuration=configuration
        )[0]
        flirt_results = flirt_run.run()
        return NIfTI.objects.get_or_create(
            path=flirt_results.out_file, parent=self, is_raw=False
        )[0]

    def calculate_mutual_information(
        self, other, histogram_bins: int = 10
    ) -> np.float64:
        return self.brain_in_mni.calculate_mutual_information(
            other.brain_in_mni, histogram_bins
        )

    @property
    def nifti(self) -> NIfTI:
        if self._nifti:
            return self._nifti
        elif not self._nifti and self.dicom:
            self._nifti = self.dicom_to_nifti()
            self.save()
            return self._nifti

    @property
    def brain(self):
        return self.extract_brain()

    @property
    def brain_in_mni(self):
        return self.register_brain_to_mni_space()

    @property
    def skull(self):
        return self.extract_skull()


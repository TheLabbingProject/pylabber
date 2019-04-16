# import numpy as np
import os
import pytz

from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_dicom.interfaces.dcm2niix import Dcm2niix
from mri.models.managers import ScanManager
from mri.models.nifti import NIfTI
from mri.models.sequence_type import SequenceType


class Scan(TimeStampedModel):
    """
    A model used to represent an MRI scan independently from the file-format in 
    which it is saved. This model handles any conversions between formats in case
    they are required, and allows for easy querying of MRI scans based on universal
    attributes.
    
    """

    time = models.DateTimeField(
        blank=True, null=True, help_text="The time in which the scan was acquired."
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="A short description of the scan's acqusition parameters.",
    )
    number = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The number of this scan relative to the session in which it was acquired.",
    )

    # Relatively universal MRI scan attributes. These might be infered from the
    # raw file's meta-data.
    echo_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between the application of the radiofrequency excitation pulse and the peak of the signal induced in the coil (in milliseconds).",
    )
    repetition_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between two successive RF pulses (in milliseconds).",
    )
    inversion_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between the 180-degree inversion pulse and the following spin-echo (SE) sequence (in milliseconds).",
    )
    spatial_resolution = ArrayField(models.FloatField(blank=True, null=True), size=3)
    sequence_type = models.ForeignKey(
        "mri.SequenceType", on_delete=models.PROTECT, blank=True, null=True
    )

    comments = models.TextField(
        max_length=1000,
        help_text="If anything noteworthy happened during acquisition, it may be noted here.",
    )

    # If this instance's origin is a DICOM file, or it was saved as one, this field
    # keeps the relation to that django_dicom.Series instance.
    dicom = models.OneToOneField(
        "django_dicom.Series",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="DICOM Series",
    )
    # Keep track of whether we've updated the instance's fields from the DICOM
    # header data.
    is_updated_from_dicom = models.BooleanField(default=False)

    # If converted to NIfTI, keep a reference to the resulting instance.
    # The reason it is suffixed with an underline is to allow for "nifti"
    # to be used as a property that automatically returns an existing instance
    # or creates one.
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
        """
        Sets instance fields from related DICOM series.
        TODO: Needs refactoring.

        Raises
        ------
        AttributeError
            If not DICOM series is related to this scan.

        Returns
        -------
        bool
            True if successful.
        """

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
            self.is_updated_from_dicom = True
            return True
        else:
            raise AttributeError(f"No DICOM data associated with MRI scan {self.id}!")

    def get_spatial_resolution_from_dicom(self) -> list:
        """
        Returns the spatial resolution of the MRI scan as infered from a
        related DICOM series. In DICOM headers, "*x*" and "*y*" resolution
        (the rows and columns of each instance) are listed as "PixelSpacing"
        and the "*z*" plane resolution corresponds to "SliceThickness".
        
        Returns
        -------
        list
            "*[x, y, z]*" spatial resolution in millimeters.
        """

        try:
            return self.dicom.pixel_spacing + [
                self.dicom.get_series_attribute("SliceThickness")
            ]
        except TypeError:
            return []

    def infer_sequence_type_from_dicom(self) -> SequenceType:
        """
        Returns the appropriate :model:`mri.SequenceType` instance according to
        the scan's "*ScanningSequence*" and "*SequenceVariant*" header values.


        Returns
        -------
        SequenceType
            A SequenceType instance.
        """

        try:
            return SequenceType.objects.get(
                scanning_sequence=self.dicom.scanning_sequence,
                sequence_variant=self.dicom.sequence_variant,
            )
        except models.ObjectDoesNotExist:
            return None

    def get_default_nifti_dir(self) -> str:
        """
        Returns the default location for the creation of a NIfTI version of the
        scan. Currently only conversion from DICOM is supported.
        
        Returns
        -------
        str
            Default location for conversion output.
        """

        if self.dicom:
            return self.dicom.get_path().replace("DICOM", "NIfTI")

    def get_default_nifti_name(self) -> str:
        """
        Returns the default file name for a NIfTI version of this scan.
        
        Returns
        -------
        str
            Default file name.
        """

        return str(self.id)

    def get_default_nifti_destination(self) -> str:
        """
        Returns the default path for a NIfTI version of this scan.
        
        Returns
        -------
        str
            Default path for NIfTI file.
        """

        directory = self.get_default_nifti_dir()
        name = self.get_default_nifti_name()
        return os.path.join(directory, name)

    def dicom_to_nifti(self, destination: str = None) -> NIfTI:
        """
        Convert this scan from DICOM to NIfTI using _dcm2niix.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Parameters
        ----------
        destination : str, optional
            The desired path for conversion output (the default is None, which
            will create the file in some default location).

        Raises
        ------
        AttributeError
            If no DICOM series is related to this scan.

        Returns
        -------
        NIfTI
            A :model:`mri.NIfTI` instance referencing the conversion output.
        """

        if self.dicom:
            dcm2niix = Dcm2niix()
            destination = destination or self.get_default_nifti_destination()
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            nifti_path = dcm2niix.convert(self.dicom.get_path(), destination)
            nifti = NIfTI.objects.create(path=nifti_path, parent=self, is_raw=True)
            return nifti
        else:
            raise AttributeError(
                f"Failed to convert scan #{self.id} from DICOM to NIfTI! No DICOM series is related to this scan."
            )

    # def extract_brain(self, configuration: BetConfiguration = None) -> NIfTI:
    #     if not configuration:
    #         configuration = BetConfiguration.objects.get_or_create(
    #             mode=BetConfiguration.ROBUST
    #         )[0]
    #     bet_run = BetRun.objects.get_or_create(
    #         in_file=self.nifti.path, configuration=configuration, output=[BetRun.BRAIN]
    #     )[0]
    #     bet_results = bet_run.run()
    #     return NIfTI.objects.get_or_create(
    #         path=bet_results.out_file, parent=self, is_raw=False
    #     )[0]

    # def extract_skull(self, configuration: BetConfiguration = None) -> NIfTI:
    #     if not configuration:
    #         configuration = BetConfiguration.objects.get_or_create(
    #             mode=BetConfiguration.ROBUST
    #         )[0]
    #     bet_run = BetRun.objects.get_or_create(
    #         in_file=self.nifti.path, configuration=configuration, output=[BetRun.SKULL]
    #     )[0]
    #     bet_results = bet_run.run()
    #     return NIfTI.objects.get_or_create(
    #         path=bet_results.skull, parent=self, is_raw=False
    #     )[0]

    # def register_brain_to_mni_space(
    #     self, configuration: FlirtConfiguration = None
    # ) -> NIfTI:
    #     if not configuration:
    #         configuration = FlirtConfiguration.objects.get_or_create()[0]
    #     fsl_path = os.environ["FSLDIR"]
    #     mni_path = os.path.join(
    #         fsl_path, "data", "standard", "MNI152_T1_1mm_brain.nii.gz"
    #     )
    #     flirt_run = FlirtRun.objects.get_or_create(
    #         in_file=self.brain.path, reference=mni_path, configuration=configuration
    #     )[0]
    #     flirt_results = flirt_run.run()
    #     return NIfTI.objects.get_or_create(
    #         path=flirt_results.out_file, parent=self, is_raw=False
    #     )[0]

    # def calculate_mutual_information(
    #     self, other, histogram_bins: int = 10
    # ) -> np.float64:
    #     return self.brain_in_mni.calculate_mutual_information(
    #         other.brain_in_mni, histogram_bins
    #     )

    @property
    def nifti(self) -> NIfTI:
        """
        Gets or creates a NIfTI version of this scan.
        
        Returns
        -------
        NIfTI
            A :model:`mri.NIfTI` instance referencing the appropriate file.
        """

        if self._nifti:
            return self._nifti
        elif not self._nifti and self.dicom:
            self._nifti = self.dicom_to_nifti()
            self.save()
            return self._nifti

    # @property
    # def brain(self):
    #     return self.extract_brain()

    # @property
    # def brain_in_mni(self):
    #     return self.register_brain_to_mni_space()

    # @property
    # def skull(self):
    #     return self.extract_skull()


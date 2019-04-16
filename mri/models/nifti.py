import nibabel as nib
import numpy as np
import os

from django.db import models
from django_extensions.db.models import TimeStampedModel
from mri.models.managers import NIfTIManager
from research.models import Subject


class NIfTI(TimeStampedModel):
    """
    A model for maintaining NIfTI_ files.

    .. _NIfTI: https://nifti.nimh.nih.gov/nifti-1/
    """

    path = models.FilePathField(max_length=500, unique=True)

    # is_raw is meant to be set according to whether the created instance
    # is the product of a direct conversion from the raw data to NIfTI (True),
    # or of a manipulation of the data (False).
    is_raw = models.BooleanField(default=False)

    # As long as this instance is the product of some conversion or manipulation
    # of a single Scan instance, this field is meant to keep a reference to that
    # instance. If it is the product of multiple Scan instances, this field may
    # be set to None, and any associated Scan instances should be reachable
    # through whichever analysis run instance they are represnted with.
    parent = models.ForeignKey(
        "mri.Scan",
        on_delete=models.CASCADE,
        related_name="derived_niftis",
        blank=True,
        null=True,
    )

    objects = NIfTIManager()

    def get_data(self) -> np.ndarray:
        """
        Uses nibabel_ to return the underlying pixel data as a NumPy_ array.
        
        .. _nibabel: https://nipy.org/nibabel/
        .. _NumPy: http://www.numpy.org/

        Returns
        -------
        np.ndarray
            Pixel data.
        """

        return nib.load(self.path).get_data()

    @property
    def b_value(self) -> list:
        """
        Returns the degree of diffusion weighting applied (b-value_) for each
        diffusion direction. This method relies on dcm2niix_'s default
        configuration in which when diffusion-weighted images (DWI_) are
        converted, another file with the same name and a "bval" extension is
        created alongside.

        .. _b-value: https://radiopaedia.org/articles/b-values-1
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI
        
        Returns
        -------
        list
            b-value for each diffusion direction.
        """

        file_name = self.path.replace("nii.gz", "bval")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            content = content.splitlines()[0].split("\t")
            return [int(value) for value in content]
        return None

    @property
    def b_vector(self) -> list:
        """
        Returns the b-vectors_ representing the diffusion weighting gradient scheme.
        This method relies on dcm2niix_'s default configuration in which when
        diffusion-weighted images (DWI_) are converted, another file with the same
        name and a "bvec" extension is created alongside.

        .. _b-vectors: https://mrtrix.readthedocs.io/en/latest/concepts/dw_scheme.html
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI
        
        Returns
        -------
        list
            b-value for each diffusion direction
        """
        file_name = self.path.replace("nii.gz", "bvec")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            return [
                [float(value) for value in vector.rstrip().split("\t")]
                for vector in content.rstrip().split("\n")
            ]
        return None

    @property
    def subject(self) -> Subject:
        """
        If this instance has a single (Scan) origin, returns the related subject.
        
        Returns
        -------
        Subject
            The subject to which this NIfTI file's origin is related with.
        """

        try:
            return self.parent.subject
        except AttributeError:
            return None

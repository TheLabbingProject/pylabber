import os

from django.db import models


class NIfTIManager(models.Manager):
    """
    A custom manager for the NIfTI model. Currently all it really does it provide
    a couple of utility methods for the automatic creation of an MNI brain instance,
    which is commonly used as a reference. This might need to find a better place.
    
    """

    def get_mni_path(self, spatial_resolution: float) -> str:
        fsl_path = os.environ["FSLDIR"]
        return os.path.join(
            fsl_path,
            "data",
            "standard",
            f"MNI152_T1_{spatial_resolution}mm_brain.nii.gz",
        )

    def get_or_create_mni(self, spatial_resolution: float):
        mni_path = self.get_mni_path(spatial_resolution)
        if os.path.isfile(mni_path):
            return self.get_or_create(path=mni_path, is_raw=False, parent=None)[0]
        return None


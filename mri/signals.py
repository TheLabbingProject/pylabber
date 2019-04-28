from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# from django_dicom.models import Series
from mri.models import Scan


# @receiver(post_save, sender=Series)
# def post_save_series_model_receiver(sender, instance, created, *args, **kwargs):
#     """
#     After a new DICOM series is created with django_dicom_, create a
#     :class:`mri.Scan` instance to represent it. This only occurs if the Series has
#     its "*is_updated*" field set to True, so that the relevant meta-data may be
#     updated for the series upon creation as well.

#     .. _django_dicom: https://github.com/ZviBaratz/django_dicom

#     Parameters
#     ----------
#     sender : type
#             The model sending the signal, in this case :class:`django_dicom.Series`.
#     instance : :class:`django_dicom.Series`
#             The instance being saved.
#     created : bool
#             Whether the instance was created in this save call.

#     """

#     if instance.is_updated:
#         scan, created = Scan.objects.get_or_create(dicom=instance)
#         return scan


@receiver(pre_save, sender=Scan)
def pre_save_scan_model_receiver(sender, instance, *args, **kwargs):
    """
    If the :class:`mri.Scan` instance has a related :class:`django_dicom.Series`
    instance with fields updated from the header, use this to infer useful
    information about the scan.

    Parameters
    ----------
    sender : type
            The model being saved, in this case :class:`mri.Scan`.
    instance : :class:`mri.Scan`
            The instance being saved.

    """

    if (
        instance.dicom
        and instance.dicom.is_updated
        and not instance.is_updated_from_dicom
    ):
        instance.update_fields_from_dicom()

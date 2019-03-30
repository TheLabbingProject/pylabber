from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_dicom.models import Series
from mri.models import Scan


@receiver(post_save, sender=Series)
def post_save_series_model_receiver(sender, instance, created, *args, **kwargs):
    if instance.is_updated:
        scan, created = Scan.objects.get_or_create(dicom=instance)
        return scan


@receiver(pre_save, sender=Scan)
def pre_save_scan_model_receiver(sender, instance, *args, **kwargs):
    if instance.dicom and instance.dicom.is_updated and not instance._nifti:
        instance.update_fields_from_dicom()

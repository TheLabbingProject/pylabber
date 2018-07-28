from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Instance)
def post_save_instance_model_receiver(sender, instance, created, *args,
                                      **kwargs):
    if created:
        try:
            instance.update_attributes_from_file()
            instance.move_file()
            instance.save()
        except Exception as e:
            print(
                'failed to update DICOM fields with the following exception:')
            print(e)


@receiver(post_save, sender=models.Patient)
def post_save_patient_model_receiver(sender, instance, created, *args,
                                     **kwargs):
    if created:
        try:
            instance.subject = instance.get_subject()
            instance.save()
        except Exception as e:
            print(
                'failed to update DICOM fields with the following exception:')
            print(e)

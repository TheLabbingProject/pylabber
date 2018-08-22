from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Instance, Patient


@receiver(post_save, sender=Instance)
def post_save_instance_model_receiver(sender, instance, created, *args,
                                      **kwargs):
    if created:
        try:
            instance.update_attributes_from_file()
            existing = Instance.objects.filter(
                instance_uid=instance.instance_uid)
            if not existing:
                instance.move_file()
                instance.save()
            else:
                Instance.objects.get(id=instance.id).delete()
        except Exception as e:
            print(
                'failed to update DICOM fields with the following exception:')
            print(e)


@receiver(post_save, sender=Patient)
def post_save_patient_model_receiver(sender, instance, created, *args,
                                     **kwargs):
    if created:
        try:
            instance.subject = instance.get_subject()
            instance.save()
        except Exception as e:
            print(
                'failed to get or create subject with the following exception:'
            )
            print(e)

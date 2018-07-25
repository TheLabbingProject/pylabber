from django.apps import AppConfig


class DicomConfig(AppConfig):
    name = 'dicom'

    def ready(self):
        import dicom.signals

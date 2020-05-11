from django.db import models
from django_dicom.models.patient import Patient

# from pylabber.plotting.providers import Providers
# from research.plotting.subject_queryset_plotter import SubjectQuerySetPlotter


class SubjectQuerySet(models.QuerySet):
    def from_dicom_patient(self, patient: Patient) -> tuple:
        data = {
            "id_number": patient.uid,
            "first_name": patient.given_name,
            "last_name": patient.family_name,
            "date_of_birth": patient.date_of_birth,
            "sex": patient.sex,
        }
        return self.get_or_create(**data)

    # def plot(
    #     self,
    #     field_name: str,
    #     provider: Providers = None,
    #     plotter_kwargs: dict = None,
    #     plot_kwargs: dict = None,
    # ):
    #     queryset = self.all()
    #     return SubjectQuerySetPlotter(queryset).plot(
    #         field_name=field_name,
    #         provider=provider,
    #         plotter_kwargs=plotter_kwargs,
    #         plot_kwargs=plot_kwargs,
    #     )

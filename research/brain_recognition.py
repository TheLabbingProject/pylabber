from django_dicom.models import Series, Patient
from django_nipype.models import FlirtConfiguration, FlirtRun

MNI_PATH = "/usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz"
cost_functions = ["MUT", "COR", "NCO", "NMU", "LSQ"]
cost_function = "MUT"


def register_all_to_mni():
    for patient in Patient.objects.all():
        # print(f"Choosing anatomical scan for {patient.patient_id}...")
        anatomical = (
            Series.objects.filter(patient=patient, description__icontains="MPRAGE")
            # .order_by("description")
            # .first()
        )
        # print(f"{anatomical.description} chosen.")
        for series in anatomical:
            if not series.nifti:
                print("Converting to NIfTI...")
                series.to_nifti()
            print(f"NIfTI exists at: {series.nifti.path}")

            print(f"Running {cost_function} FLIRT...")
            flirt_conf = FlirtConfiguration.objects.get_or_create(
                cost_function=cost_function
            )[0]
            flirt_run = FlirtRun.objects.get_or_create(
                in_file=series.nifti.path, reference=MNI_PATH, configuration=flirt_conf
            )[0]
            flirt_run.run()
            print("Done!")


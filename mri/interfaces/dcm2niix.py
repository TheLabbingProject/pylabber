import os
import subprocess

DCM2NIIX = os.getenv("DCM2NIIX")


class Dcm2niix:
    FLAGS = {"compressed": "-z", "BIDS": "-b", "name": "-f", "directory": "-o"}
    BOOLEAN = {True: "y", False: "n"}

    def __init__(self, path: str = DCM2NIIX):
        self.path = path

    def generate_command(
        self,
        path: str,
        destination: str,
        compressed: bool = True,
        generate_json: bool = True,
    ) -> list:
        directory, name = os.path.dirname(destination), os.path.basename(destination)
        return [
            self.path,
            self.FLAGS["compressed"],
            self.BOOLEAN[compressed],
            self.FLAGS["BIDS"],
            self.BOOLEAN[generate_json],
            self.FLAGS["directory"],
            directory,
            self.FLAGS["name"],
            name,
            path,
        ]

    def convert(
        self,
        path: str,
        destination: str,
        compressed: bool = True,
        generate_json: bool = False,
    ) -> str:
        command = self.generate_command(
            path, destination, compressed=compressed, generate_json=generate_json
        )
        try:
            subprocess.check_output(command)
            if os.path.isfile(f"{destination}.nii.gz"):
                return f"{destination}.nii.gz"
            else:
                raise RuntimeError(
                    "Failed to create NIfTI file using dcm2niix! Please check application configuration"
                )
        except FileNotFoundError:
            raise NotImplementedError(
                "Could not call dcm2niix! Please check settings configuration."
            )

import numpy as np

from enum import Enum
from plots.series.series_viewer.utils.plane import Plane


class CrosshairLines(Enum):
    HORIZONTAL = "h"
    VERTICAL = "v"


class CrosshairsManager:
    def __init__(self, figures: dict):
        self.figures = figures
        self.models = {}

    def get_crosshair_line_plane(self, plane: Plane, line: CrosshairLines) -> Plane:
        """
        Returns the orientation of the desired line (horizontal or vertical) for the
        given plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        line : CrosshairLines
            One of the two orientations of the crosshair lines.

        Returns
        -------
        Plane
            The plane of the crosshair line in the given plane and orientation.
        """

        return crosshair_line_dict[plane][line]

    def update_crosshair_source(
        self, plane: Plane, vertical_line: list, horizontal_line: list
    ):
        """
        Updates the crosshair's MultiLine model's source with the desired line values.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        vertical_line : list
            List of values to represent the vertical crosshair line.
        horizontal_line : list
            List of values to represent the horizontal crosshair line.
        """

        self.models[plane].data_source.data = dict(
            x=[np.arange(len(horizontal_line)), vertical_line],
            y=[horizontal_line, np.arange(len(vertical_line))],
        )


crosshair_line_dict = {
    Plane.TRANSVERSE: {
        CrosshairLines.HORIZONTAL: Plane.CORONAL,
        CrosshairLines.VERTICAL: Plane.SAGITTAL,
    },
    Plane.SAGITTAL: {
        CrosshairLines.HORIZONTAL: Plane.TRANSVERSE,
        CrosshairLines.VERTICAL: Plane.CORONAL,
    },
    Plane.CORONAL: {
        CrosshairLines.HORIZONTAL: Plane.TRANSVERSE,
        CrosshairLines.VERTICAL: Plane.SAGITTAL,
    },
}

crosshair_colors = [
    "Lime",
    "Green",
    "Black",
    "White",
    "Red",
    "Cyan",
    "Yellow",
    "Blue",
    "Orange",
    "Purple",
    "Pink",
    "Brown",
    "Indigo",
    "Grey",
]

DEFAULT_CROSSHAIR_COLOR = crosshair_colors[0]

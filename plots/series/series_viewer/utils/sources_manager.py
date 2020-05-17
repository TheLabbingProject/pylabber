import numpy as np

from bokeh.models import ColumnDataSource
from plots.series.series_viewer.utils.plane import Plane


class SourcesManager:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.sources = self.create_sources()

    def create_sources(self) -> dict:
        return {
            Plane.TRANSVERSE: {
                "image": ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
                "crosshair": ColumnDataSource(data=dict(x=[], y=[])),
            },
            Plane.SAGITTAL: {
                "image": ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
                "crosshair": ColumnDataSource(data=dict(x=[], y=[])),
            },
            Plane.CORONAL: {
                "image": ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
                "crosshair": ColumnDataSource(data=dict(x=[], y=[])),
            },
        }

    def get_image_data(self, plane: Plane, index: int) -> np.ndarray:
        """
        Returns the 2D matrix representing a single slice at a particular plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        index : int
            The index of the desired slice.

        Returns
        -------
        np.ndarray
            A 2D array of data.
        """

        image = np.take(self.data, index, axis=plane.value)
        if plane in (Plane.CORONAL, Plane.SAGITTAL):
            return np.transpose(image)
        return image

    def get_image_from_source(self, plane: Plane) -> np.ndarray:
        """
        Returns the image that is currently "loaded" to the desired plane's source.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        np.ndarray
            Current image data.
        """

        try:
            return self.sources[plane]["image"].data["image"][0]
        # If not image is loaded, returns None
        except IndexError:
            pass

    def fix_index(self, plane: Plane, index: int) -> int:
        """
        If the chosen is index is larger than the size of the image in the chosen
        plane, returns 0 instead of the given index.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        index : int
            The index to be tested against the image's shape.

        Returns
        -------
        int
            A fixed index value to use.
        """

        axis_size = self.data.shape[plane.value]
        if index >= axis_size:
            index = 0
        elif index < 0:
            index = axis_size - 1
        return index

    def create_image_data_source(self, image: np.ndarray) -> dict:
        """
        Creates a dictionary representing a single slice (index) of a plane.

        Parameters
        ----------
        image : np.ndarray
            A slice of the data in one of the three planes.

        Returns
        -------
        dict
            A dictionary representation to be used in a figure's source.
        """

        return dict(image=[image], dw=[image.shape[1]], dh=[image.shape[0]])

    def update_image_source(self, plane: Plane, image: np.ndarray):
        """
        Updates the source of the figure for the given plane with the provided image
        data.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        image : np.ndarray
            The slice data to be displayed in the figure.
        """

        self.sources[plane]["image"].data = self.create_image_data_source(image)

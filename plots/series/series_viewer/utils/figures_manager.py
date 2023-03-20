from functools import partial

import numpy as np
from bokeh.events import MouseWheel, Tap
from bokeh.io import curdoc
from bokeh.models.glyphs import Image, MultiLine
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.ranges import Range1d
from bokeh.plotting import Figure, figure
from plots.series.series_viewer.utils.crosshair import (CrosshairLines,
                                                        CrosshairsManager)
from plots.series.series_viewer.utils.palettes import (get_default_palette,
                                                       palette_dict)
from plots.series.series_viewer.utils.plane import Plane
from plots.series.series_viewer.utils.sources_manager import SourcesManager
from plots.series.series_viewer.utils.widgets_manager import WidgetsManager


class FiguresManager:
    def __init__(
        self, sources_manager: SourcesManager, widgets_manager: WidgetsManager
    ):
        self.sources_manager = sources_manager
        self.widgets_manager = widgets_manager
        self.figures = self.create_figures_dictionary()
        self.crosshairs_manager = CrosshairsManager(self.figures)

    def create_figures_dictionary(self) -> dict:
        return {
            Plane.TRANSVERSE: None,
            Plane.SAGITTAL: None,
            Plane.CORONAL: None,
        }

    def create_figure_model(self, plane: Plane) -> Figure:
        """
        Creates an instance of the Figure model for the given plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        Figure
            A Figure instance for the given plane.
        """

        figure_model = figure(
            plot_width=100,
            plot_height=100,
            x_range=[0, 100],
            y_range=[0, 100],
            title=f"{plane.name.capitalize()} View",
            name=plane.name,
        )
        figure_model.xaxis.visible = False
        figure_model.yaxis.visible = False
        return figure_model

    def create_image_model(self, plane: Plane) -> Image:
        """
        Create an instance of the Image model for the given plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        Image
            The created Image instance for the given plot.
        """

        plot = self.figures[plane].image(
            image="image",
            x=0,
            y=0,
            dw="dw",
            dh="dh",
            source=self.sources_manager.sources[plane]["image"],
            palette=get_default_palette(),
            name=f"{plane.name}_image",
        )
        return plot

    def create_crosshair_model(self, plane: Plane) -> MultiLine:
        """
        Creates an instance of the MultiLine model for the given plane to
        display a crosshair.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        MultiLine
            A model used to display the crosshair for the given plane.
        """

        crosshair = self.figures[plane].multi_line(
            "x",
            "y",
            source=self.sources_manager.sources[plane]["crosshair"],
            color="lime",
            alpha=0.4,
            line_width=1,
            name=f"{plane.name}_crosshair",
        )
        return crosshair

    def get_figure_model(self, plane: Plane) -> Figure:
        """
        Returns the existing Figure instance for the desired plane from the
        document.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        Figure
            The Figure instance for the given plane.
        """

        return curdoc().get_model_by_name(plane.name)

    def get_image_model(self, plane: Plane) -> Image:
        """
        Returns the existing Image instance for the desired plane from the
        document.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        Image
            The Image instance for the given plane.
        """

        return curdoc().get_model_by_name(f"{plane.name}_image")

    def add_wheel_interaction(self, plane: Plane):
        """
        Adds the wheel interactivity to easily browse a plane with the mouse.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        """

        self.figures[plane].on_event(
            MouseWheel,
            partial(self.widgets_manager.handle_mouse_wheel, plane=plane),
        )

    def add_click_interaction(self, plane: Plane):
        """
        Adds the click interactivity to easily browse a plane with the mouse.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        """

        self.figures[plane].on_event(
            Tap, partial(self.widgets_manager.handle_tap, plane=plane)
        )

    def update_figure_properties(self, plane: Plane, image: np.ndarray):
        """
        Updates the figure's properties according to the properties of the
        image.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        """

        width, height = image.shape[1], image.shape[0]
        figure = self.get_figure_model(plane)
        figure.plot_width = max(int(width * 1.8), 380)
        figure.plot_height = max(int(height * 1.8), 380)
        figure.x_range = Range1d(0, width)
        figure.y_range = Range1d(0, height)

    def get_crosshair_index(self, plane: Plane, line: CrosshairLines) -> int:
        """
        Returns the index of the crosshair line in the given plane and
        orientation.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        line : CrosshairLines
            One of the two possible crosshair line orientations.

        Returns
        -------
        int
            The current index of the crosshair line.
        """

        manager = self.crosshairs_manager
        crosshair_line_plane = manager.get_crosshair_line_plane(plane, line)
        return self.widgets_manager.index_sliders[crosshair_line_plane].value

    def get_crosshair_indices(self, plane: Plane):
        """
        Returns the indices of the crosshair lines in the given plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        tuple
            The indices of the crosshair lines for x and y.
        """

        x = self.get_crosshair_index(plane, CrosshairLines.VERTICAL)
        y = self.get_crosshair_index(plane, CrosshairLines.HORIZONTAL)
        return x, y

    def update_crosshair(self, plane: Plane):
        """
        Updates the crosshair for the given plane.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        """

        x, y = self.get_crosshair_indices(plane)
        image = self.sources_manager.get_image_from_source(plane)
        horizontal_line = [y] * image.shape[1]
        vertical_line = [x] * image.shape[0]
        self.crosshairs_manager.update_crosshair_source(
            plane, vertical_line, horizontal_line
        )

    def update_crosshairs(self, skip: Plane = None):
        """
        Updates the crosshair for all planes, except for the "skip" plane if
        provided.

        Parameters
        ----------
        skip : Plane, optional
            A plane to skip when updating crosshair indices, by default None
        """

        for plane in self.figures:
            if plane is not skip and isinstance(
                self.sources_manager.get_image_from_source(plane), np.ndarray
            ):
                self.update_crosshair(plane)

    def set_image(self, plane: Plane, index: int):
        """
        Sets the data for the appropriate figure according to the provided
        plane and index.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        index : int
            The index of the slice to be displayed in the figure.
        """

        image = self.sources_manager.get_image_data(plane, index)
        self.sources_manager.update_image_source(plane, image)
        self.update_figure_properties(plane, image)
        self.widgets_manager.update_values_range(plane, image)
        self.update_crosshairs(skip=plane)

    def handle_palette_change(self, attr, old, new):
        """
        Changes the figures' palette according to the user's selection.
        """

        palette = palette_dict[new]
        for plane in self.figures:
            image_model = self.get_image_model(plane)
            image_model.glyph.color_mapper = LinearColorMapper(palette=palette)

    def change_displayed_range(self, attr, old, new, plane: Plane):
        """
        Interactively changes the given plane's figure displayed range.
        """

        min_value, max_value = int(new[0]), int(new[1])
        new_image = self.sources_manager.get_image_data(
            plane, self.widgets_manager.index_sliders[plane].value
        )
        new_image[new_image >= max_value] = max_value
        new_image[new_image <= min_value] = min_value
        self.sources_manager.sources[plane]["image"].data["image"] = [
            new_image
        ]

    def handle_checkbox(self, attr, old, new):
        """
        Show or hide crosshairs and axes according to the CheckboxButtonGroup
        state.
        """

        if self.widgets_manager.get_checkbox_index("Crosshair") in new:
            self.show_crosshairs()
        else:
            self.hide_crosshairs()
        if self.widgets_manager.get_checkbox_index("Axes") in new:
            self.show_plot_axes()
        else:
            self.hide_plot_axes()

    def hide_crosshairs(self):
        """
        Hides the crosshairs in all figures.
        """

        for plane in self.figures:
            self.crosshairs_manager.models[plane].visible = False

    def show_crosshairs(self):
        """
        Shows the crosshairs in all figures.
        """

        for plane in self.figures:
            self.crosshairs_manager.models[plane].visible = True

    def hide_plot_axes(self):
        """
        Hides the axes in all figures.
        """

        for plane in self.figures:
            self.figures[plane].xaxis.visible = False
            self.figures[plane].yaxis.visible = False

    def show_plot_axes(self):
        """
        Shows the axes in all figures.
        """

        for plane in self.figures:
            self.figures[plane].xaxis.visible = True
            self.figures[plane].yaxis.visible = True

    def change_crosshair_color(self, attr, old, new):
        """
        Changes the color of the crosshairs displayed in the figures.
        """

        color = new.lower()
        for plane in self.figures:
            self.crosshairs_manager.models[plane].glyph.line_color = color

    def update_plane_index(self, attr, old, new, plane: Plane):
        self.set_image(plane, self.sources_manager.fix_index(plane, new))

    def create_figures(self):
        for plane in self.figures:
            self.figures[plane] = self.create_figure_model(plane)
            self.create_image_model(plane)
            self.crosshairs_manager.models[
                plane
            ] = self.create_crosshair_model(plane)
            self.add_wheel_interaction(plane)
            self.add_click_interaction(plane)
            slider = self.widgets_manager.create_index_slider(
                self.sources_manager.data, plane
            )
            slider.on_change(
                "value", partial(self.update_plane_index, plane=plane)
            )
            slider.visible = False
            self.widgets_manager.index_sliders[plane] = slider
            range_slider = self.widgets_manager.create_range_slider(plane)
            range_slider.visible = False
            range_slider.on_change(
                "value", partial(self.change_displayed_range, plane=plane)
            )
            self.widgets_manager.range_sliders[plane] = range_slider

import numpy as np

from bokeh.events import MouseWheel, Tap
from bokeh.models.widgets import (
    CheckboxButtonGroup,
    RangeSlider,
    Select,
    Slider,
    Toggle,
)
from plots.series.series_viewer.utils.crosshair import (
    CrosshairLines,
    crosshair_colors,
    crosshair_line_dict,
    DEFAULT_CROSSHAIR_COLOR,
)
from plots.series.series_viewer.utils.palettes import (
    DEFAULT_PALETTE,
    palette_dict,
)
from plots.series.series_viewer.utils.plane import Plane


class WidgetsManager:
    CHECKBOX_LABELS = ["Crosshair", "Axes"]

    def __init__(self):
        self.index_sliders = {}
        self.range_sliders = {}

    def create_index_slider(self, data: np.ndarray, plane: Plane) -> Slider:
        """
        Creates a slider to comfortable show and change a given plane's index.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        Slider
            An instance of the Slider model for the given plane.
        """

        slider = Slider(
            start=0,
            end=data.shape[plane.value] - 1,
            value=0,
            step=1,
            title=f"{plane.name.capitalize()} Index",
            name=f"{plane.name}_index_slider",
        )
        return slider

    def create_range_slider(self, plane: Plane) -> RangeSlider:
        """
        Creates a range slider to comfortable show and change a given plane's values
        range.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.

        Returns
        -------
        RangeSlider
            An instance of the Slider model for the given plane.
        """

        range_slider = RangeSlider(
            start=0,
            end=1,
            value=(0, 1),
            step=1,
            title=f"{plane.name.capitalize()} View",
            name=f"{plane.name}_values_slider",
        )
        return range_slider

    def handle_mouse_wheel(self, event: MouseWheel, plane: Plane):
        """
        Changes the current plane's index interactively in response to a MouseWheel
        event.

        Parameters
        ----------
        event : MouseWheel
            Rolling the mouse wheel up or down.
        plane : Plane
            One of the three planes of the 3D data.
        """

        current_value = self.index_sliders[plane].value
        if event.delta > 0:
            self.index_sliders[plane].value = current_value + 1
        elif event.delta < 0:
            self.index_sliders[plane].value = current_value - 1

    def handle_tap(self, event: Tap, plane: Plane):
        """
        Changes the other planes' indices interactively in response to a Tap event.

        Parameters
        ----------
        event : Tap
            Tapping with the mouse on a figure.
        plane : Plane
            One of the three planes of the 3D data.
        """

        x, y = int(event.x), int(event.y)
        x_plane = crosshair_line_dict[plane][CrosshairLines.VERTICAL]
        y_plane = crosshair_line_dict[plane][CrosshairLines.HORIZONTAL]
        self.index_sliders[x_plane].value = x
        self.index_sliders[y_plane].value = y

    def update_values_range(self, plane: Plane, image: np.ndarray):
        """
        Updates min and max values of the RangeSlider which corresponds to the given
        plane's figure.

        Parameters
        ----------
        plane : Plane
            One of the three planes of the 3D data.
        """

        slider = self.range_sliders[plane]
        slider.start = image.min()
        if image.max():
            slider.end = image.max()
            slider.disabled = False
        else:
            slider.end = 1
            slider.disabled = True
        slider.value = (image.min(), image.max())

    def toggle_index_sliders_visibility(self, active: bool):
        """
        Shows or hides the index sliders.

        Parameters
        ----------
        active : bool
            Index sliders' visiblity toggle button state.
        """

        for slider in self.index_sliders.values():
            slider.visible = active

    def create_index_sliders_toggle(self) -> Toggle:
        """
        Create the index sliders' visibility toggle button.

        Returns
        -------
        Toggle
            A Toggle type button instance to control index sliders' visibility.
        """

        sliders_toggle = Toggle(label="Plane Indices", active=False)
        sliders_toggle.on_click(self.toggle_index_sliders_visibility)
        return sliders_toggle

    def toggle_range_sliders_visibility(self, active: bool):
        """
        Shows or hides the range sliders.

        Parameters
        ----------
        active : bool
            Range sliders' visiblity toggle button state.
        """

        for slider in self.range_sliders.values():
            slider.visible = active

    def create_displayed_values_toggle(self):
        """
        Create the range sliders' visibility toggle button.

        Returns
        -------
        Toggle
            A Toggle type button instance to control range sliders' visibility.
        """

        displayed_values_toggle = Toggle(label="Displayed Values")
        displayed_values_toggle.on_click(self.toggle_range_sliders_visibility)
        return displayed_values_toggle

    def create_palette_select(self) -> Select:
        """
        Create a Select widget instance to choose the palette of the figures.

        Returns
        -------
        Select
            A widget to choose the desired palette for the figures.
        """

        select = Select(
            title="Palette", value=DEFAULT_PALETTE, options=list(palette_dict.keys())
        )
        # select.on_change("value", handle_palette_change)
        return select

    def create_visibility_checkbox(self) -> CheckboxButtonGroup:
        """
        Toggles crosshair and axes visiblity on or off.

        Returns
        -------
        CheckboxButtonGroup
            A button group to change the visibility of the crosshair and axes in the
            figures.
        """

        visibility_checkbox = CheckboxButtonGroup(
            labels=self.CHECKBOX_LABELS, active=[0, 2]
        )
        # visibility_checkbox.on_change("active", handle_checkbox)
        return visibility_checkbox

    def get_checkbox_index(self, label: str) -> int:
        """
        Returns the index of the given label from the CheckboxButtonGroup definition.

        Parameters
        ----------
        label : str
            The label for which the index is required.

        Returns
        -------
        int
            The index of the given label in the CheckboxButtonGroup definition.
        """

        return self.CHECKBOX_LABELS.index(label)

    def create_crosshair_color_select(self) -> Select:
        """
        Creates a widget to select the color of the crosshairs in the figures.

        Returns
        -------
        Select
            A Select widget to select between possible crosshair colors.
        """

        select = Select(
            title="Crosshair Color",
            value=DEFAULT_CROSSHAIR_COLOR,
            options=crosshair_colors,
        )
        # select.on_change("value", change_crosshair_color)
        return select

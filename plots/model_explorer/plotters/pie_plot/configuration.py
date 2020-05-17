import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColorPicker, Spinner, TextInput, Toggle, Wedge
from functools import partial
from math import pi


class PiePlotConfiguration:
    DIRECTION_TOGGLE_STATE = {
        "clock": True,
        "anticlock": False,
    }

    def __init__(self, plot: Wedge, field_name: str):
        self.plot = plot
        self.field_name = field_name
        self.source = self.plot.data_source
        self.original_angles = self.source.data["angle"].copy()
        self.x_control = self.create_x_control()
        self.y_control = self.create_y_control()
        self.color_pickers = self.create_color_pickers()
        self.label_text_inputs = self.create_label_text_inputs()
        self.radius_input = self.create_radius_input()
        self.direction_toggle = self.create_direction_toggle()

    def create_color_pickers(self) -> list:
        colors = self.source.data["color"]
        color_pickers = []
        for i, category in enumerate(self.categories):
            title = "Color" if i == 0 else ""
            picker = ColorPicker(color=colors[i], title=title, width=100)
            picker.on_change("color", partial(self.handle_color_change, i))
            color_pickers.append(picker)
        return color_pickers

    def handle_color_change(self, index: int, attr: str, old: str, new: str) -> None:
        self.source.patch({"color": [(index, new)]})

    def create_label_text_inputs(self) -> list:
        label_text_inputs = []
        for i, category in enumerate(self.categories):
            title = "Label" if i == 0 else ""
            label_text_input = TextInput(value=category, title=title, width=100)
            label_text_input.on_change(
                "value", partial(self.handle_label_text_input_change, i)
            )
            label_text_inputs.append(label_text_input)
        return label_text_inputs

    def handle_label_text_input_change(
        self, index: int, attr: str, old: str, new: str
    ) -> None:
        self.source.patch({self.field_name: [(index, new)]})

    def create_x_control(self) -> TextInput:
        x_value = self.plot.glyph.x
        x_control = Spinner(value=x_value, title="x", step=0.05, width=100)
        x_control.on_change("value", partial(self.on_coordinate_change, "x"))
        return x_control

    def create_y_control(self) -> tuple:
        y_value = self.plot.glyph.y
        y_control = Spinner(value=y_value, title="y", step=0.05, width=100)
        y_control.on_change("value", partial(self.on_coordinate_change, "y"))
        return y_control

    def on_coordinate_change(self, axis: str, attr: str, old: str, new: str) -> None:
        try:
            self.plot.glyph.update(**{axis: new})
        except ValueError:
            pass

    def create_label_and_color_grid(self) -> column:
        label_and_color = [
            row(label_text_input, color_picker)
            for label_text_input, color_picker in zip(
                self.label_text_inputs, self.color_pickers
            )
        ]
        return column(*label_and_color)

    def create_radius_input(self) -> TextInput:
        radius = self.plot.glyph.radius
        radius_input = Spinner(value=radius, title="Radius", step=0.01, width=100)
        radius_input.on_change("value", self.handle_radius_change)
        return radius_input

    def handle_radius_change(self, attr: str, old: str, new: str) -> None:
        try:
            self.plot.glyph.update(radius=new)
        except ValueError:
            pass

    def create_direction_toggle(self) -> Toggle:
        direction = self.plot.glyph.direction
        active = self.DIRECTION_TOGGLE_STATE[direction]
        toggle = Toggle(
            label=direction,
            button_type="primary",
            active=active,
            margin=(24, 0, 0, 5),
            width=100,
        )
        toggle.on_change("active", partial(self.handle_direction_change, toggle))
        return toggle

    def handle_direction_change(
        self, toggle: Toggle, attr: str, old: str, new: str
    ) -> None:
        direction = "clock" if new else "anticlock"
        angle = 2 * pi - self.source.data["angle"]
        self.plot.glyph.update(direction=direction)
        self.source.data.update(angle=angle)
        toggle.label = direction

    def create_layout(self) -> column:
        coordinates_control = row(self.x_control, self.y_control)
        radius_and_direction = row(self.radius_input, self.direction_toggle)
        label_and_color_grid = self.create_label_and_color_grid()
        return column(coordinates_control, radius_and_direction, label_and_color_grid,)

    @property
    def categories(self) -> np.ndarray:
        return self.source.data[self.field_name]

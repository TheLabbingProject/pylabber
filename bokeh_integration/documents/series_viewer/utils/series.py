import numpy as np

from bokeh.events import MouseWheel, Tap
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.widgets import (
    CheckboxButtonGroup,
    Select,
    Slider,
    Toggle,
)
from functools import partial
from .crosshair import (
    CrosshairLines,
    crosshair_colors,
    DEFAULT_CROSSHAIR_COLOR,
)
from .palettes import palette_dict, DEFAULT_PALETTE
from .plane import Plane
from .plane_figure import PlaneFigure


class Series:
    layout = row(name='main')
    figures = {
        Plane.TRANSVERSE: None,
        Plane.SAGITTAL: None,
        Plane.CORONAL: None,
    }
    sliders = {
        Plane.TRANSVERSE: None,
        Plane.SAGITTAL: None,
        Plane.CORONAL: None,
    }
    start_indices = {
        Plane.TRANSVERSE.name: [0],
        Plane.SAGITTAL.name: [0],
        Plane.CORONAL.name: [0],
    }
    palette_select = None
    visibility_checkbox = None
    histogram_toggle = None
    crosshair_color_select = None

    def __init__(self, data: np.ndarray):
        self.data = data

        self.plane_indices = ColumnDataSource(data=self.start_indices)
        self.create_plane_figure_instances()
        self.plane_indices.on_change('data', self.update_figures)
        self.update_images_from_index_source()

    def _fix_index(self, plane: Plane, index: int):
        axis_size = self.data.shape[plane.value]
        if index >= axis_size:
            index = 0
        elif index < 0:
            index = axis_size - 1
        return index

    def create_plane_figure_instances(self):
        for plane in self.figures:
            self.figures[plane] = PlaneFigure(plane=plane)

    def get_plane_index(self, plane: Plane):
        return self.plane_indices.data[plane.name][0]

    def update_plane_index(self, attr, old, new, plane: Plane):
        self.plane_indices.data[plane.name] = [new]

    def update_figures(self, attr, old, new):
        print('called')
        for plane_name in new:
            old_index = old[plane_name][0]
            new_index = new[plane_name][0]
            if old_index is not new_index:
                plane = Plane[plane_name]
                self.update_image(plane, new_index)
                self.update_crosshairs(skip=plane)

    def get_image_data(self, plane: Plane, index: int):
        return np.take(self.data, index, axis=plane.value)

    def update_image(self, plane: Plane, index: int):
        self.figures[plane].image = self.get_image_data(plane, index)

    def update_images_from_index_source(self):
        for plane in self.figures:
            self.update_image(plane, self.get_plane_index(plane))

    def get_crosshair_line_plane(self, plane: Plane, line: CrosshairLines):
        return self.figures[plane].crosshair_dict[line]

    def get_crosshair_index(self, plane: Plane, line: CrosshairLines):
        crosshair_line_plane = self.get_crosshair_line_plane(plane, line)
        return self.get_plane_index(crosshair_line_plane)

    def get_crosshair_indices(self, plane: Plane):
        x = self.get_crosshair_index(plane, CrosshairLines.VERTICAL)
        y = self.get_crosshair_index(plane, CrosshairLines.HORIZONTAL)
        return x, y

    def update_crosshair(self, plane: Plane):
        x, y = self.get_crosshair_indices(plane)
        self.figures[plane].update_crosshair(x, y)

    def update_crosshairs(self, skip: Plane = None):
        for plane in self.figures:
            if plane is not skip:
                self.update_crosshair(plane)

    def create_slider(self, plane: Plane) -> Slider:
        self.sliders[plane] = Slider(
            start=0,
            end=self.data.shape[plane.value] - 1,
            value=self.get_plane_index(plane),
            step=1,
            title=self.figures[plane].figure_model.title.text,
            name=f'{plane.name}_slider',
        )
        self.sliders[plane].on_change(
            'value', partial(self.update_plane_index, plane=plane))
        return self.sliders[plane]

    def create_sliders(self) -> None:
        for plane in self.sliders:
            self.create_slider(plane)

    def set_slider_value(self, plane: Plane, value: int):
        self.sliders[plane].value = self._fix_index(plane, value)

    def create_checkbox(self):
        self.visibility_checkbox = CheckboxButtonGroup(
            labels=['Crosshair', 'Axes'], active=[0])
        self.visibility_checkbox.on_change('active', self.handle_checkbox)
        return self.visibility_checkbox

    def remove_plot_axes(self):
        for plane in self.figures:
            self.figures[plane].figure_model.xaxis.visible = False
            self.figures[plane].figure_model.yaxis.visible = False

    def show_plot_axes(self):
        for plane in self.figures:
            self.figures[plane].figure_model.xaxis.visible = True
            self.figures[plane].figure_model.yaxis.visible = True

    def remove_crosshairs(self):
        for plane in self.figures:
            self.figures[plane].crosshair_model.visible = False

    def show_crosshairs(self):
        for plane in self.figures:
            self.figures[plane].crosshair_model.visible = True

    def create_histogram_toggle_callback(self):
        code = """
            boxes = document.getElementsByClassName("histogram_range");
            for (i = 0; i < boxes.length; i++) {
                box = boxes[i]
                if (!box.className.includes("hidden")) {box.className+=" hidden";}
                else {box.className=box.className.replace(" hidden","");}
            }
        """
        return CustomJS(code=code)

    def create_histogram_toggle(self):
        self.histogram_toggle = Toggle(label='Histogram')
        self.histogram_toggle.callback = self.create_histogram_toggle_callback(
        )
        return self.histogram_toggle

    def get_checkbox_index(self, label: str) -> int:
        return self.visibility_checkbox.labels.index(label)

    def handle_checkbox(self, attr, old, new):
        index = self.get_checkbox_index
        if index('Crosshair') in new:
            self.show_crosshairs()
        else:
            self.remove_crosshairs()
        if index('Axes') in new:
            self.show_plot_axes()
        else:
            self.remove_plot_axes()

    def create_palette_select(self):
        self.palette_select = Select(
            title='Palette',
            value=DEFAULT_PALETTE,
            options=list(palette_dict.keys()),
        )
        self.palette_select.on_change('value', self.handle_palette_change)
        return self.palette_select

    def handle_palette_change(self, attr, old, new):
        palette = palette_dict[self.palette_select.value]
        for fig in self.figures.values():
            glyph = fig.image_model.glyph
            glyph.color_mapper = LinearColorMapper(palette=palette)

    def create_plane_figure(self, plane: Plane):
        self.figures[plane].create_layout()
        self.update_crosshair(plane)
        self.add_interactions(plane)

    def add_interactions(self, plane: Plane):
        self.add_wheel_interaction(plane)
        self.add_click_interaction(plane)

    def add_wheel_interaction(self, plane: Plane):
        fig = self.figures[plane].figure_model
        fig.on_event(MouseWheel, partial(self.handle_mouse_wheel, plane=plane))

    def add_click_interaction(self, plane: Plane):
        fig = self.figures[plane].figure_model
        fig.on_event(Tap, partial(self.handle_tap, plane=plane))

    def handle_mouse_wheel(self, event: MouseWheel, plane: Plane):
        current_value = self.sliders[plane].value
        if event.delta > 0:
            self.set_slider_value(plane, current_value + 1)
        elif event.delta < 0:
            self.set_slider_value(plane, current_value - 1)

    def handle_tap(self, event: Tap, plane: Plane):
        x, y = int(event.x), int(event.y)
        x_plane = self.get_crosshair_line_plane(plane, CrosshairLines.VERTICAL)
        y_plane = self.get_crosshair_line_plane(plane,
                                                CrosshairLines.HORIZONTAL)
        self.set_slider_value(x_plane, x)
        self.set_slider_value(y_plane, y)

    def create_crosshair_color_select(self):
        self.crosshair_color_select = Select(
            title='Crosshair Color',
            value=DEFAULT_CROSSHAIR_COLOR,
            options=crosshair_colors)
        self.crosshair_color_select.on_change('value',
                                              self.change_crosshair_color)
        return self.crosshair_color_select

    def change_crosshair_color(self, attr, old, new):
        color = new.lower()
        for plane in self.figures:
            self.figures[plane].change_crosshair_color(color)

    def create_widgets(self):
        self.create_histogram_toggle()
        self.create_sliders()
        self.create_palette_select()
        self.create_crosshair_color_select()
        self.create_checkbox()

    def create_widgetbox(self):
        box = widgetbox(
            self.histogram_toggle,
            self.sliders[Plane.TRANSVERSE],
            self.sliders[Plane.SAGITTAL],
            self.sliders[Plane.CORONAL],
            self.palette_select,
            self.crosshair_color_select,
            self.visibility_checkbox,
        )
        return box

    def create_layout(self):
        figures = [fig.layout_model for fig in self.figures.values()]
        layout = row([*figures, self.create_widgetbox()], name='main')
        return layout

    def get_layout(self):
        return curdoc().get_model_by_name('main')

    @property
    def layout(self):
        return self.get_layout() or self.create_layout()

    def run(self):
        for plane in self.figures:
            self.create_plane_figure(plane)
        self.create_widgets()
        curdoc().add_root(self.layout)

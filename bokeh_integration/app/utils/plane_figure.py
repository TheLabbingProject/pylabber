import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import RangeSlider
from bokeh.plotting import figure
from .crosshair import crosshair_line_dict
from .palettes import get_default_palette
from .plane import Plane


class PlaneFigure:
    _image = None
    histogram = None

    def __init__(
            self,
            plane: Plane,
            image: np.ndarray = None,
            index: int = 0,
    ):
        self.plane = plane
        self.index = index
        self.crosshair_dict = crosshair_line_dict[self.plane]

        self.create_figure_model()
        # self.create_image_model()
        self.create_crosshair_model()
        self.create_histogram()
        if image:
            self.image = image

    def _update_image_source(self, image: np.ndarray):
        new_data = dict(
            image=[image],
            dw=[image.shape[1]],
            dh=[image.shape[0]],
        )
        self.image_model.data_source.data = new_data

    def _update_crosshair_source(self, vertical_line: list,
                                 horizontal_line: list):
        self.crosshair_model.data_source.data = dict(
            x=[self.x_range, vertical_line],
            y=[horizontal_line, self.y_range],
        )

    def create_figure_model(self):
        figure_model = figure(
            # plot_width=int(self.width * 1.8),
            # plot_height=int(self.height * 1.8),
            # x_range=[0, self.width],
            # y_range=[0, self.height],
            plot_width=100,
            plot_height=100,
            x_range=[0, 100],
            y_range=[0, 100],
            title=f'{self.plane.name.capitalize()} View',
            name=self.plane.name,
        )
        figure_model.xaxis.visible = False
        figure_model.yaxis.visible = False
        return figure_model

    def get_figure_model(self):
        return curdoc().get_model_by_name(self.plane.name)

    def create_image_model(self):
        if self.image:
            source = ColumnDataSource(
                data=dict(
                    image=[self.image],
                    dw=[self.image.shape[1]],
                    dh=[self.image.shape[0]],
                ))
        else:
            source = ColumnDataSource(data=dict(image=[], dw=[], dh=[]))
        plot = self.figure_model.image(
            image='image',
            x=0,
            y=0,
            dw='dw',
            dh='dh',
            source=source,
            palette=get_default_palette(),
            name=f'{self.plane.name}_image',
        )
        return plot

    def get_image_model(self):
        return curdoc().get_model_by_name(f'{self.plane.name}_image')

    def create_crosshair_model(self):
        source = ColumnDataSource(data=dict(x=[], y=[]))
        crosshair = self.figure_model.multi_line(
            'x',
            'y',
            source=source,
            color='black',
            alpha=0.4,
            line_width=1,
            name=f'{self.plane.name}_crosshair',
        )
        return crosshair

    def get_crosshair_model(self):
        return curdoc().get_model_by_name(f'{self.plane.name}_crosshair')

    def change_crosshair_color(self, value: str):
        crosshair = self.get_crosshair_model().glyph
        crosshair.line_color = value

    def update_crosshair(self, x: int, y: int):
        horizontal_line = [y] * self.width
        vertical_line = [x] * self.height
        self._update_crosshair_source(vertical_line, horizontal_line)

    def create_histogram(self):
        if isinstance(self.image, np.ndarray):
            min_value, max_value = self.image.min(), self.image.max()
        else:
            min_value, max_value = 0, 1
        self.histogram = RangeSlider(
            start=min_value,
            end=max_value,
            value=(min_value, max_value),
            step=1,
            title='Displayed Values',
        )
        self.histogram.on_change('value', self.change_displayed_range)
        return self.histogram

    def change_displayed_range(self, attr, old, new):
        min_value, max_value = int(new[0]), int(new[1])
        new_image = self.image.copy()
        new_image[new_image >= max_value] = max_value
        new_image[new_image <= min_value] = min_value
        self._update_image_source(new_image)

    def update_histogram_range(self):
        self.histogram.start = self.image.min()
        if self.image.max():
            self.histogram.end = self.image.max()
            self.histogram.disabled = False
        else:
            self.histogram.end = 1
            self.histogram.disabled = True
        self.histogram.value = (self.image.min(), self.image.max())

    def create_layout(self):
        layout = column(
            [
                widgetbox(
                    self.histogram, css_classes=[f'histogram_range', 'hidden'
                                                 ]), self.figure_model
            ],
            name=f'{self.plane.name}_layout')
        return layout

    def get_layout_model(self):
        return curdoc().get_model_by_name(f'{self.plane.name}_layout')

    @property
    def width(self) -> int:
        if isinstance(self.image, np.ndarray):
            return self.image.shape[1]
        return None

    @property
    def x_range(self) -> np.ndarray:
        if isinstance(self.image, np.ndarray):
            # return np.arange(self.width)
            return [0, self.width]
        return None

    @property
    def height(self) -> int:
        if isinstance(self.image, np.ndarray):
            return self.image.shape[0]
        return None

    @property
    def y_range(self) -> np.ndarray:
        if isinstance(self.image, np.ndarray):
            # return np.arange(self.height)
            return [0, self.height]
        return None

    @property
    def image(self) -> np.ndarray:
        return self._image

    @image.setter
    def image(self, value: np.ndarray) -> None:
        if self.plane in (Plane.SAGITTAL, Plane.CORONAL):
            value = np.transpose(value)
        self._image = value
        self.figure_model.plot_width = 200
        # print(type(self.figure_model.plot_width))
        # print(dir(self.figure_model))
        self.figure_model.plot_height = self.height * 2
        self.figure_model.x_range.end = self.width
        self.figure_model.y_range.end = self.height
        self._update_image_source(value)
        self.histogram.width = self.figure_model.plot_width - 40
        self.update_histogram_range()

    @property
    def figure_model(self):
        return self.get_figure_model()

    @property
    def image_model(self):
        return self.get_image_model() or self.create_image_model()

    @property
    def crosshair_model(self):
        return self.get_crosshair_model() or self.create_crosshair_model()

    @property
    def layout_model(self):
        return self.get_layout_model() or self.create_layout()

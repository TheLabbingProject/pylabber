from bokeh.layouts import column, row
from bokeh.models import FactorRange, Panel, Spinner, Tabs
from bokeh.models.plots import _list_attr_splat
from bokeh.plotting import Figure
from functools import partial
from plots.model_explorer.plotters.utils.axes.axis_configuration import (
    AxisConfiguration,
)


class AxesConfiguration:
    def __init__(self, figure: Figure):
        self.figure = figure
        self.x_range_inputs = self.create_range_inputs("x")
        self.y_range_inputs = self.create_range_inputs("y")
        self.x_axis_tabs = self.create_axis_tabs("x")
        self.y_axis_tabs = self.create_axis_tabs("y")

    def get_axes_range(self, dimension: str):
        try:
            return getattr(self.figure, f"{dimension}_range")
        except AttributeError:
            raise AttributeError(f"Failed to retrieve {dimension} axes range!")

    def create_range_start_input(self, dimension: str) -> Spinner:
        axes_range = self.get_axes_range(dimension)
        disabled = isinstance(axes_range, FactorRange)
        spinner = Spinner(
            title="Start",
            value=axes_range.start,
            step=0.05,
            width=100,
            disabled=disabled,
        )
        spinner.on_change("value", partial(self.handle_range_start_change, dimension))
        return spinner

    def handle_range_start_change(
        self, dimension: str, attr: str, old: float, new: float
    ) -> None:
        axes_range = self.get_axes_range(dimension)
        axes_range.start = new

    def create_range_end_input(self, dimension: str) -> Spinner:
        axes_range = self.get_axes_range(dimension)
        disabled = isinstance(axes_range, FactorRange)
        spinner = Spinner(
            title="End", value=axes_range.end, step=0.05, width=100, disabled=disabled
        )
        spinner.on_change("value", partial(self.handle_range_end_change, dimension))
        return spinner

    def handle_range_end_change(
        self, dimension: str, attr: str, old: float, new: float
    ) -> None:
        axes_range = self.get_axes_range(dimension)
        axes_range.end = new

    def create_range_inputs(self, dimension: str) -> row:
        range_start = self.create_range_start_input(dimension)
        range_end = self.create_range_end_input(dimension)
        return row(range_start, range_end)

    def get_axes(self, dimension: str) -> _list_attr_splat:
        try:
            return getattr(self.figure, f"{dimension}axis")
        except AttributeError:
            raise AttributeError(f"Failed to retrieve {dimension} axes!")

    def create_axis_tabs(self, dimension: str) -> Tabs:
        axes = self.get_axes(dimension)
        tabs = []
        for i, axis in enumerate(axes):
            configuration = AxisConfiguration(axis)
            layout = configuration.create_layout()
            tab = Panel(title=str(i), child=layout)
            tabs.append(tab)
        return Tabs(tabs=tabs)

    def create_layout(self) -> Panel:
        x_child = column(self.x_range_inputs, self.x_axis_tabs)
        x_axis_tab = Panel(title="x", child=x_child)
        y_child = column(self.y_range_inputs, self.y_axis_tabs)
        y_axis_tab = Panel(title="y", child=y_child)
        tabs = Tabs(tabs=[x_axis_tab, y_axis_tab])
        return Panel(title="Axes", child=tabs)

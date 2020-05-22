from bokeh.layouts import column, row
from bokeh.models import Div, Spinner, Panel, Tabs, TextInput
from bokeh.plotting import Figure
from plots.model_explorer.plotters.utils.axes.axes_configuration import (
    AxesConfiguration,
)
from plots.model_explorer.plotters.utils.legend.legend_configuration import (
    LegendConfiguration,
)


class FigureConfiguration:
    NO_LEGEND_DIV = Div(text="No legends found.")

    def __init__(self, figure: Figure):
        self.figure = figure
        self.axes_configuration = AxesConfiguration(self.figure)
        self.plot_width_input = self.create_plot_width_input()
        self.plot_height_input = self.create_plot_height_input()
        self.title_input = self.create_title_input()
        self.sizing_inputs = row(self.plot_width_input, self.plot_height_input)
        self.axes_controls = self.axes_configuration.create_layout()
        self.legend_controls = self.create_legend_controls()
        self.configuration_tabs = self.create_configuration_tabs()

    def create_title_input(self) -> TextInput:
        title = self.figure.title.text
        title_input = TextInput(title="Title", value=title, width=210)
        title_input.on_change("value", self.handle_title_change)
        return title_input

    def handle_title_change(self, attr: str, old: str, new: str) -> None:
        self.figure.title.text = new

    def create_plot_width_input(self) -> TextInput:
        plot_width = self.figure.plot_width
        plot_width_input = Spinner(title="Width", value=plot_width, step=5, width=100)
        plot_width_input.on_change("value", self.handle_plot_width_change)
        return plot_width_input

    def handle_plot_width_change(self, attr: str, old: str, new: str) -> None:
        self.figure.width = new

    def create_plot_height_input(self) -> TextInput:
        plot_height = self.figure.plot_height
        plot_height_input = Spinner(
            title="Height", value=plot_height, step=5, width=100
        )
        plot_height_input.on_change("value", self.handle_plot_height_change)
        return plot_height_input

    def handle_plot_height_change(self, attr: str, old: str, new: str) -> None:
        self.figure.height = new

    def create_legend_controls(self) -> Panel:
        if self.figure.legend:
            tabs = []
            for i, legend in enumerate(self.figure.legend):
                layout = LegendConfiguration(legend).create_layout()
                panel = Panel(title=str(i), child=layout)
                tabs.append(panel)
            legend_tabs = Tabs(tabs=tabs)
            return Panel(title="Legend", child=legend_tabs)
        return Panel(title="Legend", child=self.NO_LEGEND_DIV)

    def create_configuration_tabs(self) -> Tabs:
        tabs = [self.axes_controls, self.legend_controls]
        return Tabs(tabs=tabs)

    def create_layout(self) -> column:
        return column(self.title_input, self.sizing_inputs, self.configuration_tabs,)

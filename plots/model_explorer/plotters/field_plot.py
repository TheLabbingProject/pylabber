import pandas as pd

from bokeh.layouts import Box, column
from bokeh.models import ColumnDataSource, Panel, Tabs
from bokeh.plotting import Figure
from django.db import models
from plots.model_explorer.plotters.utils.figure_configuration import FigureConfiguration


class FieldPlot:
    CONFIGURATION_CLASS = None

    def __init__(self, field: models.Field):
        self.field = field
        self.queryset = self.field.model.objects.all()
        self.source = self.create_source()
        self.figure = self.create_figure()
        self.plot = self.create_plot()
        self.figure_configuration = FigureConfiguration(self.figure)
        self.figure_configuration_layout = self.figure_configuration.create_layout()
        self.figure_configuration_tab = Panel(
            child=self.figure_configuration_layout, title="Figure"
        )
        configuration_kwargs = self.get_configuration_kwargs()
        self.plot_configuration = self.CONFIGURATION_CLASS(**configuration_kwargs)
        self.plot_configuration_layout = self.plot_configuration.create_layout()
        self.plot_configuration_tab = Panel(
            child=self.plot_configuration_layout, title="Plot"
        )

    def get_configuration_kwargs(self) -> dict:
        return {"plot": self.plot, "field_name": self.field.name}

    def create_source(self) -> ColumnDataSource:
        records = self.queryset.values("id", self.field.name)
        series = pd.DataFrame.from_records(records, index="id").squeeze()
        series.sort_index(inplace=True)
        return ColumnDataSource(series)

    def create_figure(self) -> Figure:
        raise NotImplementedError()

    def create_plot(self) -> Figure:
        raise NotImplementedError()

    def create_layout(self) -> Box:
        configuration_tabs = Tabs(tabs=[self.figure_configuration_tab])
        return column(self.figure, configuration_tabs)

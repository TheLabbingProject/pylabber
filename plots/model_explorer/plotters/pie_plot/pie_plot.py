import pandas as pd

from bokeh.layouts import row
from bokeh.models import ColumnDataSource, Tabs, Wedge
from bokeh.palettes import Category20_20
from bokeh.plotting import figure, Figure
from bokeh.transform import cumsum
from math import pi
from plots.model_explorer.plotters.field_plot import FieldPlot
from plots.model_explorer.plotters.pie_plot.configuration import PiePlotConfiguration


class PiePlot(FieldPlot):
    CONFIGURATION_CLASS = PiePlotConfiguration

    def create_source(self) -> ColumnDataSource:
        records = self.queryset.values("id", self.field.name)
        series = pd.DataFrame.from_records(records, index="id").squeeze()
        series.sort_index(inplace=True)
        # If the field has a `choices` attribute, use it to get verbose
        # category names.
        choices = {choice[0]: choice[1] for choice in self.field.choices}
        if "" not in choices:
            choices[""] = "Unknown"
        if None not in choices:
            choices[None] = "Unknown"
        value_counts = (
            series.value_counts()
            .reset_index(name="value")
            .rename(columns={"index": self.field.name})
            .replace({self.field.name: choices})
        )
        for choice in set(choices.values()):
            if choice not in value_counts[self.field.name].values:
                value_counts = value_counts.append(
                    {self.field.name: choice, "value": 0}, ignore_index=True
                )
        value_counts["angle"] = (
            value_counts["value"] / value_counts["value"].sum() * 2 * pi
        )
        value_counts["color"] = Category20_20[: len(value_counts)]
        value_counts["percent"] = (
            value_counts["value"] / value_counts["value"].sum()
        ) * 100
        return value_counts

    def create_figure(self) -> Figure:
        tooltips = [
            (self.field.name, f"@{self.field.name}"),
            ("count", "@value"),
            ("percent", "@percent{0.00}%"),
        ]
        title = self.field.name.title()
        return figure(
            plot_height=350,
            title=title,
            toolbar_location="below",
            toolbar_sticky=False,
            tools="undo,redo,reset,save,pan,hover",
            tooltips=tooltips,
            x_range=(-0.5, 1),
            y_range=(-1, 1),
            name="field_plot",
        )

    def create_plot(self) -> Wedge:
        plot = self.figure.wedge(
            x=0,
            y=0,
            radius=0.35,
            start_angle=cumsum("angle", include_zero=True),
            end_angle=cumsum("angle"),
            line_color="white",
            fill_color="color",
            legend_field=self.field.name,
            source=self.source,
            name="main-figure",
        )
        self.figure.axis.axis_label = None
        self.figure.axis.visible = False
        self.figure.grid.grid_line_color = None
        return plot

    def create_layout(self) -> row:
        configuration_tabs = Tabs(
            tabs=[self.figure_configuration_tab, self.plot_configuration_tab]
        )
        return row(self.figure, configuration_tabs)

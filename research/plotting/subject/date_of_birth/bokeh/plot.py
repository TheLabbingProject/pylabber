import pandas as pd

from bokeh.models import ColumnDataSource, FactorRange, Range
from bokeh.plotting import figure, Figure
from bokeh.transform import dodge
from .base import DateOfBirthPlotter


class BokehDateOfBirthPlot(DateOfBirthPlotter):
    DEFAULT_PLOT_PARAMS = {
        "plot_height": 400,
        "plot_width": 1500,
        "title": "Date of Birth",
        "x_axis_label": "Year",
        "y_axis_label": "Number of Subjects",
    }

    def process_data(self) -> ColumnDataSource:
        counts = self.create_counts(self.series)
        data = counts.to_dict()
        if isinstance(self.sex, pd.Series):
            data = {
                "x": [
                    tuple([str(part) for part in index])
                    if isinstance(index, tuple)
                    else str(index)
                    for index in counts.index
                ],
                "Male": list(data["M"].values()),
                "Female": list(data["F"].values()),
            }
        else:
            data = {
                "x": [str(key) for key in data.keys()],
                "counts": list(data.values()),
            }
        return ColumnDataSource(data=data)

    def create_x_range(self) -> Range:
        if self.by_month:
            return FactorRange(*self.processed.data["x"])
        return [str(index) for index in self.processed.data["x"]]

    def create_plot(self, **kwargs) -> Figure:
        plot = figure(x_range=self.create_x_range(), **kwargs)
        if isinstance(self.sex, pd.Series):
            plot.vbar(
                x=dodge("x", -0.15, range=plot.x_range),
                top="Male",
                width=0.2,
                source=self.processed,
                color="blue",
                legend_label="Male",
            )
            plot.vbar(
                x=dodge("x", 0.15, range=plot.x_range),
                top="Female",
                width=0.2,
                source=self.processed,
                color="red",
                legend_label="Female",
            )
            plot.x_range.range_padding = 0.1
            plot.xgrid.grid_line_color = None
            plot.legend.location = "top_left"
            plot.legend.orientation = "horizontal"
        else:
            plot.vbar(
                x="x", top="counts", width=0.3, source=self.processed, color="blue"
            )
        plot.y_range.start = 0
        return plot

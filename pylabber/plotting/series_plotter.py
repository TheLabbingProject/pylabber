import pandas as pd

from pylabber.plotting.data_frame_plotter import DataFramePlotter


class SeriesPlotter(DataFramePlotter):
    def __init__(self, series: pd.Series, **kwargs):
        self.series = series
        self.processed = self.process_data()

    def process_data(self) -> pd.Series:
        return self.series

    def plot(self, **kwargs):
        kwargs = {**self.DEFAULT_PLOT_PARAMS, **kwargs}
        plot = self.create_plot(**kwargs)
        self.style_plot(plot)
        return plot

    def get_default_title(self) -> str:
        x_label = self.get_default_x_label()
        y_label = self.get_default_y_label()
        return f"{y_label} by {x_label}"

    def get_default_x_label(self) -> str:
        return self.processed.index.name.replace("_", " ").title()

    def get_default_y_label(self) -> str:
        return self.processed.name.replace("_", " ").title()

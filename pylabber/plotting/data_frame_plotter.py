import pandas as pd


class DataFramePlotter:
    FIELD_NAME = ""
    DEFAULT_PLOT_PARAMS = {}
    DEFAULT_TITLE = ""
    DEFAULT_X_LABEL = ""
    DEFAULT_Y_LABEL = ""

    def __init__(self, df: pd.DataFrame, **kwargs):
        self.df = df
        self.processed = self.process_data()

    def process_data(self) -> pd.DataFrame:
        return self.df

    def create_plot(self, **kwargs):
        raise NotImplementedError()

    def style_plot(self, plot) -> None:
        pass

    def plot(self, **kwargs):
        kwargs = {**self.DEFAULT_PLOT_PARAMS, **kwargs}
        plot = self.create_plot(**kwargs)
        self.style_plot(plot)
        return plot

    def get_default_title(self) -> str:
        return self.DEFAULT_TITLE

    def get_default_x_label(self) -> str:
        return self.DEFAULT_X_LABEL

    def get_default_y_label(self) -> str:
        return self.DEFAULT_Y_LABEL

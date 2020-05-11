import matplotlib.pyplot as plt
import pandas as pd

from research.plotting.subject.date_of_birth.base import DateOfBirthPlotter


class MatplotlibDateOfBirthPlotter(DateOfBirthPlotter):
    DEFAULT_PLOT_PARAMS = {
        "color": ("red", "blue"),
        "grid": False,
        "figsize": (15, 7),
        "rot": 30,
        "title": "Dates of Birth",
    }
    SEX_LEGEND_LABELS = "Female", "Male"

    def __init__(
        self,
        series: pd.Series,
        bins: str = "y",
        x_label: str = "",
        y_label: str = "",
        sex: pd.Series = None,
    ):
        super().__init__(
            series=series, bins=bins, x_label=x_label, y_label=y_label, sex=sex,
        )
        if isinstance(self.sex, pd.Series):
            self.DEFAULT_PLOT_PARAMS["legend"] = True

    def process_data(self) -> pd.DataFrame:
        return self.create_counts(self.series)

    def sparsify_ticks(self, plot: plt.Subplot) -> None:
        ticks = plot.xaxis.get_ticklocs()
        ticklabels = [l.get_text()[1:5] for l in plot.xaxis.get_ticklabels()]
        plot.xaxis.set_ticks(ticks[::12])
        plot.xaxis.set_ticklabels(ticklabels[::12])

    def style_plot(self, plot: plt.Subplot) -> None:
        # Set axis labels.
        plot.set_xlabel(self.x_label or self.DEFAULT_X_LABEL)
        plot.set_ylabel(self.y_label or self.DEFAULT_Y_LABEL)
        # Change y-axis ticks to show integers instead of floats.
        plot.locator_params(axis="y", integer=True)
        # Sparsify ticks if plotting by month.
        if self.by_month:
            self.sparsify_ticks(plot)
        if isinstance(self.sex, pd.Series):
            plot.legend(labels=self.SEX_LEGEND_LABELS)

    def create_plot(self, **kwargs) -> plt.Subplot:
        return self.processed.plot(kind="bar", **kwargs)

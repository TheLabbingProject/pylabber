import numpy as np
import pandas as pd

from .series_plotter import SeriesPlotter


class DateOfBirthPlotter(SeriesPlotter):
    MONTH_BIN_INDICATORS = "m", "month", "months"
    MONTHS = np.arange(1, 13)
    DEFAULT_X_LABEL = "Year"
    DEFAULT_Y_LABEL = "Number of Subjects"

    def __init__(
        self,
        series: pd.Series,
        bins: str = "y",
        x_label: str = "",
        y_label: str = "",
        sex: pd.Series = None,
        **kwargs,
    ):
        self.bins = bins.lower().strip()
        self.by_month = self.bins in self.MONTH_BIN_INDICATORS
        self.x_label = x_label
        self.y_label = y_label
        self.sex = sex
        self.by_sex: bool = isinstance(self.sex, pd.Series)
        super().__init__(series, **kwargs)

    def create_index(self, counts: pd.Series):
        years = counts.index
        if self.by_month or self.by_sex:
            years = counts.index.levels[0]
        if self.by_month:
            years = np.arange(min(years), max(years) + 1)
        if self.by_month and self.by_sex:
            return pd.MultiIndex.from_product(
                [years, self.MONTHS, self.sex.unique()],
                names=["year", "month", self.sex.name],
            )
        elif self.by_month:
            return pd.MultiIndex.from_product(
                [years, self.MONTHS], names=["year", "month"]
            )
        else:
            if self.by_sex:
                return pd.MultiIndex.from_product(
                    [years, self.sex.unique()], names=["year", self.sex.name]
                )
            return pd.Index(years, name="year")

    def create_counts(self, series: pd.Series) -> pd.DataFrame:
        dates = series.dropna().astype("datetime64")
        if self.by_month and self.by_sex:
            counts = dates.groupby([dates.dt.year, dates.dt.month, self.sex]).count()
        elif self.by_month:
            counts = dates.groupby([dates.dt.year, dates.dt.month]).count()
        elif self.by_sex:
            counts = dates.groupby([dates.dt.year, self.sex]).count()
        else:
            counts = dates.groupby(dates.dt.year).count()
        index = self.create_index(counts)
        counts = counts.reindex(index).fillna(0)
        if self.by_sex:
            return self.pivot_by_sex(counts)
        return counts

    def pivot_by_sex(self, series: pd.Series) -> pd.DataFrame:
        series = series.reset_index(self.sex.name)
        if isinstance(series.index, pd.MultiIndex):
            index = [level.name for level in series.index.levels]
        else:
            index = series.index.name
        return series.pivot_table(
            columns=self.sex.name, values=self.series.name, index=index
        )

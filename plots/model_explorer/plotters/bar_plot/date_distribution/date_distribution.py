import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, FactorRange, Tabs
from bokeh.palettes import Category10_10
from bokeh.plotting import Figure, figure
from django.db.models import Field
from plots.model_explorer.plotters.bar_plot.bar_plot import BarPlot
from plots.model_explorer.plotters.bar_plot.date_distribution import (
    DateDistributionConfiguration,
)
from plots.model_explorer.plotters.bar_plot.date_distribution.time_bins import (
    TimeBins,
)
from titlecase import titlecase


class DateDistribution(BarPlot):
    CONFIGURATION_CLASS = DateDistributionConfiguration
    DEFAULT_FIGURE_CONFIG = {
        "plot_height": 400,
        "plot_width": 1000,
        "toolbar_location": "above",
        "y_axis_label": "Count",
    }
    INDEX_NAMES = {
        TimeBins.DAY: (
            TimeBins.YEAR.value,
            TimeBins.MONTH.value,
            TimeBins.DAY.value,
        ),
        TimeBins.MONTH: (TimeBins.YEAR.value, TimeBins.MONTH.value),
        TimeBins.YEAR: (TimeBins.YEAR.value,),
    }
    NAME = "bk-date-dist"

    def __init__(
        self,
        field: Field,
        time_bin: TimeBins = TimeBins.YEAR,
        by: Field = None,
    ):
        self.date_counts = None
        self.time_bin = time_bin
        self.by = by
        self.stackers = ["Count"]
        super().__init__(field)
        self.plot_configuration.time_bin_select.on_change(
            "active", self.handle_time_bin_change
        )

    def get_configuration_kwargs(self) -> dict:
        kwargs = super().get_configuration_kwargs()
        kwargs["time_bin"] = self.time_bin
        return kwargs

    def compose_default_title(self) -> str:
        field_name = self.field.name.replace("_", " ")
        time_bin = self.time_bin.value
        return titlecase(f"{field_name} Count by {time_bin}")

    def count_dates(self, df: pd.DataFrame) -> dict:
        df[self.field.name] = df[self.field.name].astype("datetime64")
        min_date = min(df[self.field.name].dropna())
        max_date = max(df[self.field.name].dropna())
        index = pd.date_range(min_date, max_date)
        if not isinstance(self.by, Field):
            df = df.groupby(df[self.field.name].dt.date).count()
            df = df.reindex(index, fill_value=0)
            return {"Count": df}
        else:
            df = df.groupby(
                [df[self.field.name].dt.date, df[self.by.name]]
            ).count()
            level_values = df.index.get_level_values(self.by.name)
            levels = list(set(level_values))
            self.stackers = levels
            counts = {}
            for level in levels:
                level_counts = df[level_values == level]
                level_counts = level_counts.reset_index(self.by.name).drop(
                    self.by.name, 1
                )
                level_counts = level_counts.reindex(index, fill_value=0)
                counts[level] = level_counts
            return counts

    def get_records_fields(self) -> tuple:
        if isinstance(self.by, Field):
            return "id", self.field.name, self.by.name
        else:
            return "id", self.field.name

    def create_data(self) -> pd.DataFrame:
        fields = self.get_records_fields()
        records = self.queryset.values(*fields)
        df = pd.DataFrame.from_records(records, index="id")
        self.date_counts = self.count_dates(df)
        data = {}
        for category, date_count in self.date_counts.items():
            group_by = self.get_counts_group_by(date_count)
            counts = date_count.groupby(group_by).sum()
            levels = []
            if hasattr(counts.index, "levels"):
                for i in range(len(counts.index.levels)):
                    levels.append(counts.index.levels[i].astype(str))
                counts.index = counts.index.set_levels(levels)
            else:
                counts.index = counts.index.astype(str)
            data[category] = counts[self.field.name].values
        data["factors"] = counts.index.values
        return data

    def get_counts_group_by(self, category: pd.DataFrame) -> list:
        if self.time_bin == TimeBins.DAY:
            return [
                category.index.year,
                category.index.month,
                category.index.day,
            ]
        elif self.time_bin == TimeBins.MONTH:
            return [category.index.year, category.index.month]
        elif self.time_bin == TimeBins.YEAR:
            return [category.index.year]

    def create_source(self) -> ColumnDataSource:
        data = self.create_data()
        return ColumnDataSource(data=data)

    def create_figure(self) -> Figure:
        title = self.compose_default_title()
        factors = self.source.data["factors"]
        return figure(
            x_range=FactorRange(*factors),
            title=title,
            x_axis_label=self.time_bin.value,
            **self.DEFAULT_FIGURE_CONFIG,
            name="bk-date-dist-figure",
        )

    def create_plot(self) -> list:
        color = Category10_10[: len(self.stackers)]
        vbar = self.figure.vbar_stack(
            self.stackers,
            x="factors",
            width=0.9,
            source=self.source,
            color=color,
            legend_label=self.stackers,
            name="main-figure",
        )
        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0.1
        self.figure.xaxis.major_label_orientation = 1
        self.figure.xgrid.grid_line_color = None
        if isinstance(self.by, Field):
            self.figure.legend.title = titlecase(self.by.name)
        if len(self.stackers) == 1:
            self.figure.legend.visible = False
        return vbar

    def handle_time_bin_change(self, attr: str, old: int, new: int) -> None:
        self.time_bin = list(self.INDEX_NAMES.keys())[new]
        self.__init__(self.field, self.time_bin)
        layout = self.create_layout()
        main_layout = curdoc().get_model_by_name("main-layout")
        main_layout.children[1] = layout

    def create_layout(self) -> row:
        configuration_tabs = Tabs(
            tabs=[self.figure_configuration_tab, self.plot_configuration_tab]
        )
        return row(self.figure, configuration_tabs, name="bk-date-dist")

    @property
    def layout(self) -> row:
        return curdoc().get_model_by_name("bk-date-dist")

    @property
    def index_names(self) -> tuple:
        return self.INDEX_NAMES.get(self.time_bin)

    @property
    def source_index_key(self) -> str:
        return "_".join(self.index_names)

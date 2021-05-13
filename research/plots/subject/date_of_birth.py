import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, figure
from django.db.models import QuerySet
from research.plots.subject.sex_pie import SEX_COLORS, SEX_VALUES

FIELDS = "date_of_birth", "sex"
TOOLTIPS = [("Year", "@year"), ("Sex", "$name"), ("Count", "@$name")]


def plot_bokeh_date_of_birth(queryset: QuerySet) -> Figure:
    values = queryset.values_list(*FIELDS)
    df = pd.DataFrame(values, columns=FIELDS)
    df["date_of_birth"] = df["date_of_birth"].astype("datetime64")
    df["sex"] = df["sex"].replace(SEX_VALUES)
    counts = df.groupby([df["date_of_birth"].dt.year, "sex"]).count()
    counts.columns = ["count"]
    years = counts.index.levels[0].astype(int).to_numpy()
    try:
        years = range(years.min(), years.max() + 1)
    except ValueError:
        return
    sexes = list(df["sex"].unique())
    index = pd.MultiIndex.from_product([years, sexes])
    counts = counts.reindex(index, fill_value=0)
    counts.index.names = ["year", "sex"]
    data = counts.unstack().droplevel(0, axis=1)
    source = ColumnDataSource(data=data)
    p = figure(
        title="Date of Birth Distribution by Sex",
        x_axis_label="Year",
        y_axis_label="Count",
        plot_height=250,
        plot_width=700,
        toolbar_location="above",
        tooltips=TOOLTIPS,
    )
    color = [SEX_COLORS.get(sex) for sex in sexes]
    p.vbar_stack(
        stackers=sexes,
        x="year",
        width=0.9,
        color=color,
        legend_label=sexes,
        source=source,
    )
    p.legend.location = "top_left"
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    return p

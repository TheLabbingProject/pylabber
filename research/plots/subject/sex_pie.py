from math import pi

import pandas as pd
from bokeh.plotting import Figure, figure
from bokeh.transform import cumsum
from django.db.models import QuerySet

SEX_VALUES = {
    "M": "Male",
    "F": "Female",
    "": "Unknown",
    None: "Unknown",
    "U": "Other",
}
SEX_COLORS = pd.Series(
    {"Male": "orange", "Female": "green", "Other": "brown", "Unknown": "grey"},
    name="color",
)


def plot_bokeh_sex_pie(queryset: QuerySet) -> Figure:
    values = list(queryset.values("sex"))
    data = (
        pd.DataFrame(values)
        .replace({"sex": SEX_VALUES})
        .value_counts()
        .reset_index(name="value")
        .rename(columns={"index": "sex"})
        .merge(SEX_COLORS, left_on="sex", right_index=True)
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    p = figure(
        plot_height=250,
        plot_width=350,
        title="Sex",
        toolbar_location=None,
        tools="hover",
        tooltips="@sex: @value",
        x_range=(-0.5, 1.0),
    )
    p.wedge(
        x=0,
        y=1,
        radius=0.3,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="sex",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    return p

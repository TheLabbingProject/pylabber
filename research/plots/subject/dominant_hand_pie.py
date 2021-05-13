from math import pi

import pandas as pd
from bokeh.plotting import Figure, figure
from bokeh.transform import cumsum
from django.db.models import QuerySet

DOMINANT_HAND_VALUES = {
    "R": "Right",
    "L": "Left",
    "A": "Ambidextrous",
    "": "Unknown",
    None: "Unknown",
}
DOMINANT_HAND_COLORS = pd.Series(
    {
        "Right": "blue",
        "Left": "red",
        "Ambidextrous": "purple",
        "Unknown": "grey",
    },
    name="color",
)


def plot_bokeh_dominant_hand_pie(queryset: QuerySet) -> Figure:
    values = list(queryset.values("dominant_hand"))
    data = (
        pd.DataFrame(values)
        .replace(DOMINANT_HAND_VALUES)
        .value_counts()
        .reset_index(name="value")
        .rename(columns={"index": "dominant_hand"})
        .merge(DOMINANT_HAND_COLORS, left_on="dominant_hand", right_index=True)
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    p = figure(
        plot_height=250,
        plot_width=350,
        title="Dominant Hand",
        toolbar_location=None,
        tools="hover",
        tooltips="@dominant_hand: @value",
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
        legend_field="dominant_hand",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    return p


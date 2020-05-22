from bokeh.layouts import row
from bokeh.models import Div, VBar


class BarPlotConfigration:
    def __init__(self, plot: VBar, field_name: str):
        self.plot = plot
        self.field_name = field_name
        self.source = self.plot.data_source

    def create_layout(self) -> row:
        div = Div(text="")
        return row(div)

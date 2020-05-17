from bokeh.layouts import column, row
from bokeh.models import Axis, FactorRange, Panel, Spinner
from plots.model_explorer.plotters.utils.text.configuration import (
    TextPropertiesConfiguration,
)


class AxisConfiguration:
    def __init__(self, axis: Axis):
        self.axis = axis
        self.text_properties = self.create_text_properties()

    def create_text_properties(self) -> column:
        text_props = TextPropertiesConfiguration(self.axis)
        return text_props.create_layout()

    def create_layout(self) -> Panel:
        return column(self.text_properties)

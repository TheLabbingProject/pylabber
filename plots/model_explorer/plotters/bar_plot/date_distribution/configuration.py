from bokeh.layouts import column
from bokeh.models import ColorPicker, Div, RadioButtonGroup
from functools import partial
from plots.model_explorer.plotters.bar_plot.configuration import BarPlotConfigration
from plots.model_explorer.plotters.bar_plot.date_distribution.time_bins import TimeBins


class DateDistributionConfiguration(BarPlotConfigration):
    TIME_BIN_LABELS = [TimeBins.DAY.value, TimeBins.MONTH.value, TimeBins.YEAR.value]

    def __init__(self, plot: list, field_name: str, time_bin: TimeBins):
        self.plot = plot
        self.field_name = field_name
        self.source = self.plot[0].data_source
        self.time_bin = time_bin
        self.time_bin_title = Div(text="Bins")
        self.time_bin_select = self.create_time_bin_select()
        self.color_pickers = self.create_color_pickers()

    def create_time_bin_select(self) -> RadioButtonGroup:
        active = self.TIME_BIN_LABELS.index(self.time_bin.value)
        rbg = RadioButtonGroup(labels=self.TIME_BIN_LABELS, active=active, width=210)
        return rbg

    def create_color_pickers(self) -> column:
        color_pickers = []
        for i, plot in enumerate(self.plot):
            picker = ColorPicker(color=plot.glyph.fill_color, width=100)
            picker.on_change("color", partial(self.handle_color_change, i))
            color_pickers.append(picker)
        return column(*color_pickers)

    def handle_color_change(self, index: int, attr: str, old: str, new: str) -> None:
        self.plot[index].glyph.fill_color = new

    def create_layout(self) -> column:
        return column(self.time_bin_title, self.time_bin_select, self.color_pickers)

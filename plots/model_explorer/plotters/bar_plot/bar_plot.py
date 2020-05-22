from plots.model_explorer.plotters.field_plot import FieldPlot
from plots.model_explorer.plotters.bar_plot.configuration import BarPlotConfigration


class BarPlot(FieldPlot):
    CONFIGURATION_CLASS = BarPlotConfigration

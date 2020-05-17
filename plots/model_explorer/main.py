from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Div
from bokeh.plotting import Figure
from django.apps import apps
from django.db import models
from plots.model_explorer.plotters.bar_plot.date_distribution import DateDistribution
from plots.model_explorer.plotters.field_plot import FieldPlot
from plots.model_explorer.plotters.pie_plot.pie_plot import PiePlot
from plots.model_explorer.utils.field_selector import FieldSelector


class ModelExplorer:
    STARTUP_DIV = Div(text="", name="main-figure")
    NO_PLOT_DIV = Div(text="No plot available.", name="main-figure")

    def __init__(self, field_selector: FieldSelector):
        self.field_selector = field_selector
        self.field_selector.field_select.on_change("value", self.handle_field_selection)
        self.loading_div = Div(text="Loading...", name="loading-div")
        self.content = column(self.STARTUP_DIV, name="content")

    def get_plotter(self, field: models.Field) -> FieldPlot:
        is_char_field = isinstance(field, models.CharField)
        n_distinct = (
            field.model.objects.order_by(field.name).distinct(field.name).count()
        )
        if is_char_field and (field.choices or n_distinct < 12):
            return PiePlot
        elif type(field) == models.DateField:
            return DateDistribution

    def handle_field_selection(self, attr: str, old: str, new: str) -> None:
        self.content.children = [self.loading_div]
        field = self.field_selector.selected_field
        Plotter = self.get_plotter(field)
        layout = Plotter(field).create_layout() if Plotter else self.NO_PLOT_DIV
        layout.name = "main-figure"
        self.content.children = [layout]

    def create_layout(self):
        field_select_layout = field_selector.create_layout()
        return row(field_select_layout, self.content, name="main-layout")

    @property
    def layout(self):
        return curdoc().get_model_by_name("main-layout")

    @property
    def main_figure(self) -> Figure:
        return curdoc().get_model_by_name("main-figure")


curdoc().clear()
app_models = apps.get_models()
field_selector = FieldSelector(app_models)
model_explorer = ModelExplorer(field_selector=field_selector)
layout = model_explorer.create_layout()
curdoc().add_root(layout)
selected_field = field_selector.field_select.value
model_explorer.handle_field_selection("value", selected_field, selected_field)

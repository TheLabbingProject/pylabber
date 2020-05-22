from bokeh.layouts import column
from bokeh.models import (
    Div,
    Legend,
    Select,
    Panel,
    RadioButtonGroup,
    Tabs,
    TextInput,
)
from functools import partial
from plots.model_explorer.plotters.utils.orientation import Orientation
from plots.model_explorer.plotters.utils.text.configuration import (
    TextPropertiesConfiguration,
)
from plots.model_explorer.plotters.utils.legend.legend_location import LegendLocation


class LegendConfiguration:
    ORIENTATION_LABELS = [orientation.value for orientation in Orientation]

    def __init__(self, legend: Legend):
        self.legend = legend
        self.location_select = self.create_location_select()
        self.orientation_group = self.create_orientation_group()
        self.title_text_configuration = TextPropertiesConfiguration(
            self.legend, "title"
        )
        self.title_input = self.create_title_input()
        self.label_text_configuration = TextPropertiesConfiguration(
            self.legend, "label"
        )
        self.title_panel = self.create_title_panel()
        self.label_inputs = self.create_label_inputs()
        self.labels_panel = self.create_labels_panel()
        self.configuration_tabs = self.create_configuration_tabs()

    def create_location_select(self) -> Select:
        location = (
            self.legend.location if self.legend.visible else LegendLocation.NONE.name
        )
        location_select = Select(
            title="Location",
            value=location,
            options=LegendLocation.options(),
            width=210,
        )
        location_select.on_change("value", self.handle_location_change)
        return location_select

    def handle_location_change(self, attr: str, old: str, new: str) -> None:
        if new == LegendLocation.NONE.name:
            self.legend.visible = False
        else:
            self.legend.update(location=new)
            if old == LegendLocation.NONE.name:
                self.legend.visible = True

    def create_orientation_group(self) -> RadioButtonGroup:
        orientation = self.legend.orientation.title()
        active = self.ORIENTATION_LABELS.index(orientation)
        button_group = RadioButtonGroup(
            labels=self.ORIENTATION_LABELS, active=active, width=210
        )
        button_group.on_change("active", self.handle_orientation_change)
        return button_group

    def handle_orientation_change(self, attr: str, old: str, new: str) -> None:
        orientation = self.ORIENTATION_LABELS[new].lower()
        self.legend.orientation = orientation

    def create_title_input(self) -> TextInput:
        title = self.legend.title
        title_input = TextInput(title="Title", value=title, width=210)
        title_input.on_change("value", self.handle_title_change)
        title_input.trigger("value", title, title)
        return title_input

    def handle_title_change(self, attr: str, old: str, new: str) -> None:
        self.legend.title = new
        if not new:
            self.title_text_configuration.disable_all()
        elif new and not old:
            self.title_text_configuration.enable_all()

    def create_title_panel(self) -> Panel:
        text_configuration_layout = self.title_text_configuration.create_layout()
        layout = column(self.title_input, text_configuration_layout)
        return Panel(title="Title", child=layout)

    def read_item_label(self, index: int) -> str:
        label = self.legend.items[index].label
        if isinstance(label, str):
            return label
        elif isinstance(label, dict):
            value = list(label.values())[0]
            return f"${value}"

    def create_label_inputs(self) -> column:
        inputs = []
        for i, label_item in enumerate(self.legend.items):
            value = self.read_item_label(i)
            disabled = value.startswith("$")
            label_input = TextInput(value=value, disabled=disabled, width=210)
            label_input.on_change("value", partial(self.handle_label_item_change, i))
            inputs.append(label_input)
        title = Div(text="Labels")
        return column(title, *inputs)

    def handle_label_item_change(
        self, index: int, attr: str, old: str, new: str
    ) -> None:
        self.legend.items[index] = new

    def create_labels_panel(self) -> Panel:
        text_configuration_layout = self.label_text_configuration.create_layout()
        layout = column(self.label_inputs, text_configuration_layout)
        return Panel(title="Items", child=layout)

    def create_configuration_tabs(self) -> Tabs:
        tabs = [self.title_panel, self.labels_panel]
        return Tabs(tabs=tabs)

    def create_layout(self) -> column:
        return column(
            self.location_select, self.orientation_group, self.configuration_tabs,
        )

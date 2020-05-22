from bokeh.layouts import column, row
from bokeh.models import (
    Axis,
    ColorPicker,
    Div,
    Label,
    Model,
    RadioButtonGroup,
    Select,
    Spinner,
    Title,
)
from plots.model_explorer.plotters.utils.text.font import Font
from plots.model_explorer.plotters.utils.text.font_style import FontStyle
from plots.model_explorer.plotters.utils.text.horizontal_alignment import (
    HorizontalAlignment,
)
from plots.model_explorer.plotters.utils.text.vertical_alignment import (
    VerticalAlignment,
)
from plots.model_explorer.plotters.utils.orientation import Orientation
from plots.model_explorer.plotters.utils.text.text_properties import TextProperties


class TextPropertiesConfiguration:
    PREFIX = {Axis: "axis_label", Label: "label", Title: "title"}
    HORIZONTAL_ALIGNMENT = (
        HorizontalAlignment.left,
        HorizontalAlignment.center,
        HorizontalAlignment.right,
    )
    VERTICAL_ALIGNMENT = (
        VerticalAlignment.top,
        VerticalAlignment.middle,
        VerticalAlignment.bottom,
        VerticalAlignment.alphabetic,
        VerticalAlignment.hanging,
    )
    OPTIONALS = (
        "horizontal_alignment_select",
        "vertical_alignment_select",
        "standoff_spinner",
    )
    ORIENTATION_LABELS = [orientation.value for orientation in Orientation]

    def __init__(self, model: Model, prefix: str = None):
        self.model = model
        self.prefix = prefix or self.get_prefix()
        self.font_select = self.create_font_select()
        self.style_select = self.create_style_select()
        self.size_spinner = self.create_size_spinner()
        self.color_picker = self.create_color_picker()
        self.alpha_spinner = self.create_alpha_spinner()
        if isinstance(self.model, Label):
            self.horizontal_alignment_select = self.create_horizontal_alignment_select()
            self.vertical_alignment_select = self.create_vertical_alignment_select()
            self.alignment_controls = self.create_alignment_controls()
            self.extra_contols = self.alignment_controls
        elif isinstance(self.model, Axis):
            self.standoff_spinner = self.create_standoff_spinner()
            self.extra_contols = self.standoff_spinner
        else:
            self.extra_contols = Div(text="")

    def get_prefix(self) -> str:
        for _type, prefix in self.PREFIX.items():
            if isinstance(self.model, _type):
                return prefix
        else:
            raise TypeError(f"Invalid model type ({type(self.model)})!")

    def create_font_select(self) -> Select:
        select = Select(
            title="Font", value=self.text_font, options=Font.options(), width=210
        )
        select.on_change("value", self.handle_font_change)
        return select

    def handle_font_change(self, attr: str, old: str, new: str) -> None:
        setattr(self.model, self.text_font_name, new)

    def create_style_select(self) -> Select:
        style_select = Select(
            title="Style",
            value=self.text_font_style,
            options=FontStyle.options(),
            width=100,
        )
        style_select.on_change("value", self.handle_style_change)
        return style_select

    def handle_style_change(self, attr: str, old: str, new: str) -> None:
        setattr(self.model, self.text_font_style_name, new)

    def create_size_spinner(self) -> Spinner:
        value = int(self.text_font_size[:-2])
        spinner = Spinner(title="Size", value=value, low=0, step=1, width=100)
        spinner.on_change("value", self.handle_size_change)
        return spinner

    def handle_size_change(self, attr: str, old: float, new: float) -> None:
        setattr(self.model, self.text_font_size_name, f"{new}pt")

    def create_color_picker(self) -> ColorPicker:
        picker = ColorPicker(title="Color", color=self.text_color, width=100)
        picker.on_change("color", self.handle_color_change)
        return picker

    def handle_color_change(self, attr: str, old: str, new: str) -> None:
        setattr(self.model, self.text_color_name, new)

    def create_alpha_spinner(self) -> Spinner:
        spinner = Spinner(
            title="Alpha", value=self.text_alpha, low=0, high=1, step=0.05, width=100
        )
        spinner.on_change("value", self.handle_alpha_change)
        return spinner

    def handle_alpha_change(self, attr: str, old: float, new: float) -> None:
        setattr(self.model, self.text_alpha_name, new)

    def create_horizontal_alignment_select(self) -> RadioButtonGroup:
        value = HorizontalAlignment[self.text_align]
        active = self.HORIZONTAL_ALIGNMENT.index(value)
        h_align_select = RadioButtonGroup(
            labels=["Left", "Center", "Right"],
            active=active,
            width=210,
            disabled=isinstance(self.model, Axis),
        )
        h_align_select.on_change("active", self.handle_horizontal_align_change)
        return h_align_select

    def handle_horizontal_align_change(self, attr: str, old: int, new: int) -> None:
        value = self.HORIZONTAL_ALIGNMENT[new].name
        setattr(self.model, self.text_align_name, value)

    def create_vertical_alignment_select(self) -> Select:
        v_align_select = Select(
            value=self.text_baseline,
            options=VerticalAlignment.options(),
            width=210,
            disabled=isinstance(self.model, Axis),
        )
        v_align_select.on_change("value", self.handle_vertical_align_change)
        return v_align_select

    def handle_vertical_align_change(self, attr: str, old: str, new: str) -> None:
        setattr(self.model, self.text_baseline_name, new)

    def create_alignment_controls(self) -> column:
        title = Div(text="Alignment")
        return column(
            title, self.horizontal_alignment_select, self.vertical_alignment_select,
        )

    def create_standoff_spinner(self) -> Spinner:
        spinner = Spinner(title="Standoff", value=self.standoff, width=210)
        spinner.on_change("value", self.handle_standoff_change)
        return spinner

    def handle_standoff_change(self, attr: str, old: float, new: float) -> None:
        setattr(self.model, self.standoff_name, new)

    def create_layout(self) -> column:
        style_and_size = row(self.style_select, self.size_spinner)
        color_and_alpha = row(self.color_picker, self.alpha_spinner)
        return column(
            self.font_select, style_and_size, color_and_alpha, self.extra_contols
        )

    def disable_all(self) -> None:
        self.font_select.disabled = True
        self.style_select.disabled = True
        self.size_spinner.disabled = True
        self.color_picker.disabled = True
        self.alpha_spinner.disabled = True
        for widget in self.OPTIONALS:
            try:
                attribute = getattr(self, widget)
            except AttributeError:
                pass
            else:
                attribute.disabled = True

    def enable_all(self) -> None:
        self.font_select.disabled = False
        self.style_select.disabled = False
        self.size_spinner.disabled = False
        self.color_picker.disabled = False
        self.alpha_spinner.disabled = False
        for widget in self.OPTIONALS:
            try:
                attribute = getattr(self, widget)
            except AttributeError:
                pass
            else:
                attribute.disabled = False

    @property
    def text_font_name(self) -> str:
        return f"{self.prefix}_{TextProperties.FONT.value}"

    @property
    def text_font(self) -> str:
        return getattr(self.model, self.text_font_name)

    @property
    def text_font_size_name(self) -> str:
        return f"{self.prefix}_{TextProperties.SIZE.value}"

    @property
    def text_font_size(self) -> str:
        return getattr(self.model, self.text_font_size_name)

    @property
    def text_font_style_name(self) -> str:
        return f"{self.prefix}_{TextProperties.STYLE.value}"

    @property
    def text_font_style(self) -> str:
        return getattr(self.model, self.text_font_style_name)

    @property
    def text_color_name(self) -> str:
        return f"{self.prefix}_{TextProperties.COLOR.value}"

    @property
    def text_color(self) -> str:
        return getattr(self.model, self.text_color_name)

    @property
    def text_alpha_name(self) -> str:
        return f"{self.prefix}_{TextProperties.ALPHA.value}"

    @property
    def text_alpha(self) -> str:
        return getattr(self.model, self.text_alpha_name)

    @property
    def text_align_name(self) -> str:
        return f"{self.prefix}_{TextProperties.ALIGN.value}"

    @property
    def text_align(self) -> str:
        return getattr(self.model, self.text_align_name)

    @property
    def text_baseline_name(self) -> str:
        return f"{self.prefix}_{TextProperties.BASELINE.value}"

    @property
    def text_baseline(self) -> str:
        return getattr(self.model, self.text_baseline_name)

    @property
    def standoff_name(self) -> str:
        return f"{self.prefix}_{TextProperties.STANDOFF.value}"

    @property
    def standoff(self) -> str:
        return getattr(self.model, self.standoff_name, None)

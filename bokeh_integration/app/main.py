import numpy as np

from bokeh.events import MouseWheel, Tap
from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure, Figure
from bokeh.models.widgets import (
    CheckboxButtonGroup,
    # DataTable,
    RangeSlider,
    Select,
    Slider,
    # TableColumn,
    Toggle,
)
from functools import partial
from utils.crosshair import (
    CrosshairLines,
    crosshair_colors,
    crosshair_line_dict,
    DEFAULT_CROSSHAIR_COLOR,
)
from utils.palettes import DEFAULT_PALETTE, get_default_palette, palette_dict
from utils.plane import Plane

data = np.load('data.npy')


def get_image_data(plane: Plane, index: int):
    image = np.take(data, index, axis=plane.value)
    if plane in (Plane.CORONAL, Plane.SAGITTAL):
        return np.transpose(image)
    return image


figures = {
    Plane.TRANSVERSE: None,
    Plane.SAGITTAL: None,
    Plane.CORONAL: None,
}

sources = {
    Plane.TRANSVERSE: {
        'image': ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
        'crosshair': ColumnDataSource(data=dict(x=[], y=[])),
    },
    Plane.SAGITTAL: {
        'image': ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
        'crosshair': ColumnDataSource(data=dict(x=[], y=[])),
    },
    Plane.CORONAL: {
        'image': ColumnDataSource(data=dict(image=[], dw=[], dh=[])),
        'crosshair': ColumnDataSource(data=dict(x=[], y=[])),
    },
}


def get_image_from_source(plane: Plane) -> np.ndarray:
    try:
        return sources[plane]['image'].data['image'][0]
    except IndexError:
        pass


def fix_index(plane: Plane, index: int):
    axis_size = data.shape[plane.value]
    if index >= axis_size:
        index = 0
    elif index < 0:
        index = axis_size - 1
    return index


def update_plane_index(attr, old, new, plane: Plane):
    set_image(plane, fix_index(plane, new))


def create_figure_model(plane: Plane):
    figure_model = figure(
        plot_width=100,
        plot_height=100,
        x_range=[0, 100],
        y_range=[0, 100],
        title=f'{plane.name.capitalize()} View',
        name=plane.name,
    )
    figure_model.xaxis.visible = False
    figure_model.yaxis.visible = False
    return figure_model


def get_figure_model(plane: Plane) -> Figure:
    return curdoc().get_model_by_name(plane.name)


def create_image_model(plane: Plane):
    plot = figures[plane].image(
        image='image',
        x=0,
        y=0,
        dw='dw',
        dh='dh',
        source=sources[plane]['image'],
        palette=get_default_palette(),
        name=f'{plane.name}_image',
    )
    return plot


def get_image_model(plane: Plane):
    return curdoc().get_model_by_name(f'{plane.name}_image')


def create_toggle_callback(css_name: str):
    code = f"""
        boxes = document.getElementsByClassName("{css_name}");
        for (i = 0; i < boxes.length; i++) {{
            box = boxes[i]
            if (!box.className.includes("hidden")) {{box.className+=" hidden";}}
            else {{box.className=box.className.replace(" hidden","");}}
        }}
    """
    return CustomJS(code=code)


def create_index_sliders_toggle():
    sliders_toggle = Toggle(label='Plane Indices')
    sliders_toggle.callback = create_toggle_callback('plane_indices')
    return sliders_toggle


def create_displayed_values_toggle():
    displayed_values_toggle = Toggle(label='Displayed Values')
    displayed_values_toggle.callback = create_toggle_callback(
        'displayed_values')
    return displayed_values_toggle


# def create_sizing_toggle():
#     sizing_toggle = Toggle(label='Sizing')
#     sizing_toggle.callback = create_toggle_callback('image_sizing')
#     return sizing_toggle

# table_data = dict(
#     planes=['Transverse', 'Sagittal', 'Coronal'],
#     width=[100, 100, 100],
#     height=[100, 100, 100],
# )
# table_source = ColumnDataSource(table_data)

# def create_sizing_table():
#     columns = [
#         TableColumn(
#             field='planes',
#             title='Plane',
#         ),
#         TableColumn(
#             field='width',
#             title='% Width',
#         ),
#         TableColumn(
#             field='height',
#             title='% Height',
#         ),
#     ]
#     data_table = DataTable(
#         source=table_source,
#         columns=columns,
#         editable=True,
#         index_position=None,
#         width=255,
#         height=100,
#         name='sizing_table',
#     )
#     return data_table

# def update_image_sizing_from_table(attr, old, new):
#     for i, plane_name in enumerate(new['planes']):
#         plane_name = plane_name.upper()
#         plane = Plane[plane_name]
#         image = get_image_from_source(plane)
#         figure_model = get_figure_model(plane)
#         image_model = get_image_model(plane)
#         width = int((int(new['width'][i]) / 100) * image.shape[1])
#         height = int((int(new['height'][i]) / 100) * image.shape[0])
#         print('before', figure_model.plot_width)
#         figure_model.plot_width = width
#         print('after', figure_model.plot_width)
#         figure_model.plot_height = height
#         image_model.glyph.dw = width
#         image_model.glyph.dh = height

# sizing_table = create_sizing_table()
# table_source.on_change('data', update_image_sizing_from_table)

# def get_sizing_table_model():
#     return curdoc().get_model_by_name('sizing_table')


def create_palette_select():
    select = Select(
        title='Palette',
        value=DEFAULT_PALETTE,
        options=list(palette_dict.keys()),
    )
    select.on_change('value', handle_palette_change)
    return select


def handle_palette_change(attr, old, new):
    palette = palette_dict[new]
    for plane in figures:
        image_model = get_image_model(plane)
        image_model.glyph.color_mapper = LinearColorMapper(palette=palette)


def create_crosshair_model(plane: Plane):
    crosshair = figures[plane].multi_line(
        'x',
        'y',
        source=sources[plane]['crosshair'],
        color='black',
        alpha=0.4,
        line_width=1,
        name=f'{plane.name}_crosshair',
    )
    return crosshair


def get_crosshair_model(plane: Plane):
    return curdoc().get_model_by_name(f'{plane.name}_crosshair')


def get_crosshair_line_plane(plane: Plane, line: CrosshairLines):
    return crosshair_line_dict[plane][line]


def get_crosshair_index(plane: Plane, line: CrosshairLines):
    crosshair_line_plane = get_crosshair_line_plane(plane, line)
    return index_sliders[crosshair_line_plane].value


def get_crosshair_indices(plane: Plane):
    x = get_crosshair_index(plane, CrosshairLines.VERTICAL)
    y = get_crosshair_index(plane, CrosshairLines.HORIZONTAL)
    return x, y


def update_crosshair_source(
        plane: Plane,
        vertical_line: list,
        horizontal_line: list,
):
    crosshair_model = get_crosshair_model(plane)
    crosshair_model.data_source.data = dict(
        x=[np.arange(len(horizontal_line)), vertical_line],
        y=[horizontal_line, np.arange(len(vertical_line))],
    )


def update_crosshair(plane: Plane):
    x, y = get_crosshair_indices(plane)
    image = get_image_from_source(plane)
    horizontal_line = [y] * image.shape[1]
    vertical_line = [x] * image.shape[0]
    update_crosshair_source(plane, vertical_line, horizontal_line)


def update_crosshairs(skip: Plane = None):
    for plane in figures:
        if plane is not skip and isinstance(
                get_image_from_source(plane), np.ndarray):
            update_crosshair(plane)


def add_wheel_interaction(plane: Plane):
    figures[plane].on_event(MouseWheel, partial(
        handle_mouse_wheel, plane=plane))


def add_click_interaction(plane: Plane):
    figures[plane].on_event(Tap, partial(handle_tap, plane=plane))


def handle_mouse_wheel(event: MouseWheel, plane: Plane):
    current_value = index_sliders[plane].value
    if event.delta > 0:
        index_sliders[plane].value = current_value + 1
    elif event.delta < 0:
        index_sliders[plane].value = current_value - 1


def handle_tap(event: Tap, plane: Plane):
    x, y = int(event.x), int(event.y)
    x_plane = crosshair_line_dict[plane][CrosshairLines.VERTICAL]
    y_plane = crosshair_line_dict[plane][CrosshairLines.HORIZONTAL]
    index_sliders[x_plane].value = x
    index_sliders[y_plane].value = y


def create_index_slider(plane: Plane) -> Slider:
    slider = Slider(
        start=0,
        end=data.shape[plane.value] - 1,
        value=0,
        step=1,
        title=f'{plane.name.capitalize()} Index',
        name=f'{plane.name}_index_slider',
    )
    return slider


def create_range_slider(plane: Plane) -> RangeSlider:
    range_slider = RangeSlider(
        start=0,
        end=1,
        value=(0, 1),
        step=1,
        title=f'{plane.name.capitalize()} View',
        name=f'{plane.name}_values_slider',
    )
    return range_slider


def create_image_data_source(image: np.ndarray) -> dict:
    return dict(image=[image], dw=[image.shape[1]], dh=[image.shape[0]])


def update_image_source(plane: Plane, image: np.ndarray) -> None:
    sources[plane]['image'].data = create_image_data_source(image)


def update_figure_properties(plane: Plane):
    image = get_image_from_source(plane)
    width, height = image.shape[1], image.shape[0]
    fig = get_figure_model(plane)
    fig.plot_width = min(int(width * 1.8), 405)
    fig.plot_height = int(height * 1.8)
    fig.x_range = Range1d(0, width)
    fig.y_range = Range1d(0, height)


def set_image(plane: Plane, index: int):
    image = get_image_data(plane, index)
    update_image_source(plane, image)
    update_figure_properties(plane)
    update_crosshairs(skip=plane)
    update_values_range(plane)


def update_values_range(plane: Plane):
    slider = range_sliders[plane]
    image = get_image_from_source(plane)
    slider.start = image.min()
    if image.max():
        slider.end = image.max()
        slider.disabled = False
    else:
        slider.end = 1
        slider.disabled = True
    slider.value = (image.min(), image.max())


def change_displayed_range(attr, old, new, plane: Plane):
    min_value, max_value = int(new[0]), int(new[1])
    new_image = get_image_data(plane, index_sliders[plane].value)
    new_image[new_image >= max_value] = max_value
    new_image[new_image <= min_value] = min_value
    sources[plane]['image'].data['image'] = [new_image]


CHECKBOX_LABELS = ['Crosshair', 'Axes']


def create_visibility_checkbox():
    visibility_checkbox = CheckboxButtonGroup(
        labels=CHECKBOX_LABELS, active=[0, 2])
    visibility_checkbox.on_change('active', handle_checkbox)
    return visibility_checkbox


def get_checkbox_index(label: str) -> int:
    return CHECKBOX_LABELS.index(label)


def handle_checkbox(attr, old, new):
    if get_checkbox_index('Crosshair') in new:
        show_crosshairs()
    else:
        hide_crosshairs()
    if get_checkbox_index('Axes') in new:
        show_plot_axes()
    else:
        hide_plot_axes()


def hide_plot_axes():
    for plane in figures:
        figures[plane].xaxis.visible = False
        figures[plane].yaxis.visible = False


def show_plot_axes():
    for plane in figures:
        figures[plane].xaxis.visible = True
        figures[plane].yaxis.visible = True


def hide_crosshairs():
    for plane in figures:
        get_crosshair_model(plane).visible = False


def show_crosshairs():
    for plane in figures:
        get_crosshair_model(plane).visible = True


def create_crosshair_color_select():
    select = Select(
        title='Crosshair Color',
        value=DEFAULT_CROSSHAIR_COLOR,
        options=crosshair_colors)
    select.on_change('value', change_crosshair_color)
    return select


def change_crosshair_color(attr, old, new):
    color = new.lower()
    for plane in figures:
        get_crosshair_model(plane).glyph.line_color = color


index_sliders = {}
range_sliders = {}
for plane in figures:
    figures[plane] = create_figure_model(plane)
    create_image_model(plane)
    create_crosshair_model(plane)
    add_wheel_interaction(plane)
    add_click_interaction(plane)
    slider = create_index_slider(plane)
    slider.on_change('value', partial(update_plane_index, plane=plane))
    index_sliders[plane] = slider
    range_slider = create_range_slider(plane)
    range_slider.on_change('value', partial(
        change_displayed_range, plane=plane))
    range_sliders[plane] = range_slider

figures_row = row(*figures.values())

extra_widgets = widgetbox(
    create_visibility_checkbox(),
    create_palette_select(),
    create_crosshair_color_select(),
)

main_layout = row(
    figures_row,
    column(
        create_index_sliders_toggle(),
        widgetbox(
            *index_sliders.values(),
            css_classes=['plane_indices', 'hidden'],
        ),
        create_displayed_values_toggle(),
        widgetbox(
            *range_sliders.values(),
            css_classes=['displayed_values', 'hidden'],
        ),
        extra_widgets,
    ),
    # sizing_mode='scale_both',
    name='main',
)
curdoc().add_root(main_layout)

for plane in figures:
    set_image(plane, 0)

import pydicom
from bokeh.layouts import row
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
)
from bokeh.plotting import figure, curdoc
# from ..models import Instance

# def plot_instance(instance: Instance):
# image = instance.read_data().pixel_array
image = pydicom.dcmread(
    '/home/flavus/Projects/pylabber/media/304848286/1.3.12.2.1107.5.2.43.66024.2016120813261380400095647.0.0.0/34.dcm'
).pixel_array
source = ColumnDataSource(data=dict(image=[image]))
# Create figure
plot = figure(
    plot_width=image.shape[1] * 10,
    plot_height=image.shape[0] * 10,
    x_range=[0, image.shape[1]],
    y_range=[0, image.shape[0]],
    name='instance_figure',
)

# Plot image
plot.image(
    image='image',
    x=0,
    y=0,
    dw=image.shape[1],
    dh=image.shape[0],
    source=source,
    palette='Spectral11',
    name='instance_plot',
)

# Add hover tool
hover = HoverTool(tooltips=[('x', '$x'), ('y', '$y'), ('value', '@image')])
plot.add_tools(hover)

layout = row(plot)
curdoc().add_root(layout)

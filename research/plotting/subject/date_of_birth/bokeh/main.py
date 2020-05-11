import pandas as pd

from bokeh.plotting import curdoc
from .plot import BokehDateOfBirthPlot


args = curdoc().session_context.request.arguments
series = pd.Series(args.get("dates", []), dtype="datetime64[ns]")
plot = BokehDateOfBirthPlot(series=series).plot()
curdoc().add_root(plot)

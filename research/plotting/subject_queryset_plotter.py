# from pylabber.plotting.queryset_plotter import QuerySetPlotter
# from pylabber.plotting.providers import Providers
# from research.plotting.subject.date_of_birth.bokeh.plot import BokehDateOfBirthPlot
# from research.plotting.subject.date_of_birth.matplotlib import (
#     MatplotlibDateOfBirthPlotter,
# )
# from research.plotting.subject.sex.bokeh import BokehSexPlotter
# from research.plotting.subject.sex.matplotlib import MatplotlibSexPlotter


# class SubjectQuerySetPlotter(QuerySetPlotter):
#     PLOTTERS = {
#         None: {
#             Providers.BOKEH: None,
#             Providers.MATPLOTLIB: None,
#             Providers.SEABORN: None,
#         },
#         "date_of_birth": {
#             Providers.BOKEH: BokehDateOfBirthPlot,
#             Providers.MATPLOTLIB: MatplotlibDateOfBirthPlotter,
#             Providers.SEABORN: None,
#         },
#         "sex": {
#             Providers.BOKEH: BokehSexPlotter,
#             Providers.MATPLOTLIB: MatplotlibSexPlotter,
#             Providers.SEABORN: None,
#         },
#     }

import pandas as pd

from django.db.models import QuerySet
from pylabber.plotting.providers import Providers


class QuerySetPlotter:
    PLOTTERS = {
        None: {
            Providers.BOKEH: None,
            Providers.MATPLOTLIB: None,
            Providers.SEABORN: None,
        }
    }
    PK_FIELD = "id"

    def __init__(self, queryset: QuerySet, provider: Providers = Providers.MATPLOTLIB):
        self.queryset = queryset
        self.provider = provider

    def get_plotter(self, field_name: str = None, provider: Providers = None):
        provider = provider if isinstance(provider, Providers) else self.provider
        try:
            return self.PLOTTERS[field_name][provider]
        except KeyError as e:
            key = e.args[0]
            if field_name == key:
                name = self.__class__.__name__
                raise NotImplementedError(
                    f"{field_name} is not registered in {name}'s PLOTTERS dictionary.'"
                )
            elif provider == key:
                raise NotImplementedError(
                    f"Plotting {field_name} with {provider.value} is not supported :("
                )
            else:
                raise

    def convert_queryset_to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame.from_records(self.queryset.values())
        if not df.empty:
            df.set_index(self.PK_FIELD, inplace=True)
            df.sort_index(inplace=True)
        return df

    def plot(
        self,
        field_name: str = None,
        provider: Providers = None,
        plotter_kwargs: dict = None,
        plot_kwargs: dict = None,
    ):
        df = self.convert_queryset_to_dataframe()
        series = df[field_name].copy()
        plotter_kwargs = plotter_kwargs if isinstance(plotter_kwargs, dict) else {}
        for column in df.columns:
            if plotter_kwargs.get(column):
                plotter_kwargs[column] = df[column].copy()
        if series.any():
            plotter = self.get_plotter(field_name=field_name, provider=provider)
            plot_kwargs = plot_kwargs if isinstance(plot_kwargs, dict) else {}
            return plotter(series, **plotter_kwargs).plot(**plot_kwargs)

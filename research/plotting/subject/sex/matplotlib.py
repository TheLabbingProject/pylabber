import matplotlib.pyplot as plt

from research.plotting.subject.sex.base import SexPlotter


class MatplotlibSexPlotter(SexPlotter):
    COLORS = {
        "Male": "cyan",
        "Female": "magenta",
        "Other": "yellow",
        "Unknown": "white",
    }

    def create_plot(self) -> plt.Subplot:
        plot = self.processed.plot.pie(
            y="count",
            x="sex",
            colors=self.processed["colors"],
            labels=self.processed["labels"],
            autopct="%.2f",
            title="Sex",
        )
        plot.set_ylabel("")
        return plot

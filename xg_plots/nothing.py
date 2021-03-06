import pandas as pd
from bokeh.colors import RGB
from bokeh.models import Span
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components


def return_one():
    return 1


def add_line_two_sd(p, location):
    first_line = Span(
        location=location,
        dimension="height",
        line_color=RGB(255, 140, 0, 0.2),
        line_dash="dashed",
        line_width=3,
    )
    p.add_layout(first_line)
    return p


def add_line_three_sd(p, location):
    first_line = Span(
        location=location,
        dimension="height",
        line_color=RGB(255, 69, 0),
        line_dash="dashed",
        line_width=3,
    )
    p.add_layout(first_line)
    return p


class Plotter_Step_Goals_and_xG:
    def __init__(self):
        self.cleaned_player = None
        self.name = None

    def set_player(self, path, name):
        self.name = name
        player = pd.read_csv(path)
        selected_columns = ["Date", "Goals", "xG", "Match", "Minutes played"]
        just_mx = player["Competition"] == "Mexico. Liga MX"
        self.cleaned_player = player[just_mx][selected_columns]
        self.cleaned_player["player"] = name
        self.cleaned_player["Date"] = pd.to_datetime(self.cleaned_player["Date"])
        self.__data = ColumnDataSource(self.cleaned_player)

    def plot_step_goals_and_xG(self, TOOLTIPS, color="blue"):
        p = figure(
            x_axis_type="datetime",
            title=f"Goles de {self.name} en la Liga MX",
            x_axis_label="Fecha",
            y_axis_label="Goles",
            tooltips=TOOLTIPS,
        )
        p.step(x="Date", y="Goals", source=self.__data, color=color)
        p.line(x="Date", y="Goals", source=self.__data, color=RGB(54, 162, 235, 0.0))
        return components(p)

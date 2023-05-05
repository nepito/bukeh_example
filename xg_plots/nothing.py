import pandas as pd
from bokeh.colors import RGB
from bokeh.models import Span
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.models import Panel


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


def add_horizontal_line(p, location):
    first_line = Span(
        location=location,
        dimension="width",
        line_width=1,
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
            sizing_mode = "scale_both",
            aspect_ratio = 1,
            toolbar_location=None,
        )
        p.step(x="Date", y="Goals", source=self.__data, color=color)
        p.line(x="Date", y="Goals", source=self.__data, color=RGB(54, 162, 235, 0.0))
        return components(p)


def add_patch_color(p, x, y, color):
    p.patch(
        x,
        y,
        color=RGB(*color),
        line_width=0,
    )
    return p


def direct_metrics(p, x, color):
    y = [9, 13, 13, 9]
    return add_patch_color(p, x, y, color)


def indirect_metrics(p, x, color):
    y = [0, 6, 6, 0]
    return add_patch_color(p, x, y, color)


def good_direct_metrics(p):
    x = [1, 1, 2, 2]
    color = [154, 205, 50, 0.1]
    return direct_metrics(p, x, color)


def better_direct_metrics(p):
    x = [2, 2, 3, 3]
    color = [154, 205, 50, 0.3]
    return direct_metrics(p, x, color)


def bad_direct_metrics(p):
    x = [-2, -2, -1, -1]
    color = [255, 140, 0, 0.1]
    return direct_metrics(p, x, color)


def worst_direct_metrics(p):
    x = [-3, -3, -2, -2]
    color = [255, 140, 0, 0.3]
    return direct_metrics(p, x, color)


def add_patch_to_direct_metrics(p):
    p = bad_direct_metrics(p)
    p = worst_direct_metrics(p)
    p = good_direct_metrics(p)
    p = better_direct_metrics(p)
    return p


pd.set_option("mode.chained_assignment", None)


class Plotter_Intervals_From_Rivals:
    def __init__(self, path, team):
        self.team = team
        self.read_data(path)
        self.teams = self.metrics.rival.unique()

    def read_data(self, path):
        self.metrics = pd.read_csv(path)

    def plot_intervals(self, round, TOOLTIPS):
        self.get_groups_and_source(round)
        self.get_metrics_from_round_and_team(round, TOOLTIPS)
        self.plot_annual_metrics()
        return self.setup_axis_style(round)

    def get_groups_and_source(self, round):
        team = self.teams[-round]
        metrics = self.metrics[self.metrics.rival == team]
        metrics.loc[:, ("max")] = metrics.loc[:, ("values")] + 0.1
        self.group = metrics.groupby("metrics")
        self.source = ColumnDataSource(self.group)
        self.group = metrics[::-1]["metrics"]

    def get_metrics_from_round_and_team(self, round, TOOLTIPS):
        team = self.teams[-round]
        self.p = figure(
            y_range=self.group,
            x_range=(-4, 5.5),
            width=500,
            height=550,
            toolbar_location=None,
            tools="hover",
            tooltips=TOOLTIPS,
            title=f"Métricas de {self.team} \n Jornada {round}: {team}",
        )
        self.p.title.text_font_size = "12pt"

    def plot_annual_metrics(self):
        self.p.hbar(y="metrics", left="values_max", right="max_max", height=0.4, source=self.source)
        self.p = add_patch_color(self.p, [1, 1, 2, 2], [0, 6, 6, 0], [255, 140, 0, 0.1])
        self.p = add_patch_color(self.p, [2, 2, 3, 3], [0, 6, 6, 0], [255, 140, 0, 0.3])
        self.p = add_patch_color(self.p, [-2, -2, -1, -1], [0, 6, 6, 0], [154, 205, 50, 0.1])
        self.p = add_patch_color(self.p, [-3, -3, -2, -2], [0, 6, 6, 0], [154, 205, 50, 0.3])
        self.p = add_patch_to_direct_metrics(self.p)
        self.p = add_line_two_sd(self.p, -2)
        self.p = add_line_two_sd(self.p, 2)
        self.p = add_line_three_sd(self.p, -3)
        self.p = add_line_three_sd(self.p, 3)
        self.p = add_horizontal_line(self.p, 6)
        self.p = add_horizontal_line(self.p, 9)

    def setup_axis_style(self, round):
        titulo = self.teams[-round]
        self.p.xaxis.minor_tick_line_color = None
        self.p.ygrid.grid_line_color = None
        self.p.outline_line_color = None
        tab = Panel(child=self.p, title=titulo)
        return tab


COLOR = {
    "Morelia": ["#FFC300", "#DF0404"],
    "Cimarrones": ["#718dbf", "#e84d60"],
    "Raya2": ["#191970", "#C0C0C0"],
    "Correcaminos": ["#FF4500", "#191970"],
}


COLOR_IN_TEXT = {
    "Morelia": ["amarillo", "rojo"],
    "Cimarrones": ["azul", "rojo"],
    "Raya2": ["azul", "gris"],
    "Correcaminos": ["naranja", "azul"],
}

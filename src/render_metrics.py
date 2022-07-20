import pandas as pd
from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.colors import RGB
from xg_plots import Plotter_Step_Goals_and_xG

metrics = pd.read_csv("data/normalized_metrics.csv")


def get_player(path, name):
    player = pd.read_csv(path)
    selected_columns = ["Date", "Goals", "xG", "Match", "Minutes played"]
    just_mx = player["Competition"] == "Mexico. Liga MX"
    cleaned_player = player[just_mx][selected_columns]
    cleaned_player["player"] = name
    cleaned_player["Date"] = pd.to_datetime(cleaned_player["Date"])
    return cleaned_player


plotter = Plotter_Step_Goals_and_xG()
plotter.set_player("data/berterame_wyscout.csv", "Germán Berterame")
aguirre = get_player("data/aguirre_wyscout.csv", "Rodrigo Aguirre")
janssen = get_player("data/janssen_wyscout.csv", "Vincent Janssen")
ibanez = get_player("data/ibanez_wyscout.csv", "Nico Ibáñez")
TOOLTIPS = [
    ("Partido", "@{Match}"),
    ("Minutos Jugados", "@{Minutes played}"),
    ("xG", "@{xG}"),
]
data2 = ColumnDataSource(aguirre)
data3 = ColumnDataSource(janssen)
data4 = ColumnDataSource(ibanez)
script, div = plotter.plot_step_goals_and_xG(TOOLTIPS)

plot_ra = figure(
    x_axis_type="datetime",
    title="Goles de Aguirre en la Liga MX",
    x_axis_label="Fecha",
    y_axis_label="Goles",
    tooltips=TOOLTIPS,
)
plot_ra.step(x="Date", y="Goals", source=data2, color="red")
plot_ra.line(x="Date", y="Goals", source=data2, color=RGB(54, 162, 235, 0.0))
script_ra, div_ra = components(plot_ra)

plot_vj = figure(
    x_axis_type="datetime",
    title="Goles de Janssen en la Liga MX",
    x_axis_label="Fecha",
    y_axis_label="Goles",
    tooltips=TOOLTIPS,
)
plot_vj.step(x="Date", y="Goals", source=data3, color="green")
plot_vj.line(x="Date", y="Goals", source=data3, color=RGB(54, 162, 235, 0.0))
script_vj, div_vj = components(plot_vj)

plot_ni = figure(
    x_axis_type="datetime",
    title="Goles de Ibáñez en la Liga MX",
    x_axis_label="Fecha",
    y_axis_label="Goles",
    tooltips=TOOLTIPS,
)
plot_ni.step(x="Date", y="Goals", source=data4, color="yellow")
plot_ni.line(x="Date", y="Goals", source=data4, color=RGB(54, 162, 235, 0.0))
script_ni, div_ni = components(plot_ni)


def get_str_metrics(index):
    mind_metrics = [
        "player_minutes",
        "goal_total",
        "goal_assists",
        "passes_key",
        "shots_on",
        "dribbles_success",
        "tackles_interceptions",
    ]
    metrics_of_player_1 = list(metrics.loc[index][mind_metrics])
    str_player_1 = [str(metric) for metric in metrics_of_player_1]
    return str.join(", ", str_player_1)


fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

all_players = {f"player_{player+1}": get_str_metrics(player) for player in range(4)}
rendered = env.get_template("ejemplo_1.html").render(
    script=script,
    div=div,
    script_ra=script_ra,
    div_ra=div_ra,
    script_vj=script_vj,
    div_vj=div_vj,
    script_ni=script_ni,
    div_ni=div_ni,
    **all_players,
)
print(rendered)

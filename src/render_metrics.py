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


TOOLTIPS = [
    ("Partido", "@{Match}"),
    ("Minutos Jugados", "@{Minutes played}"),
    ("xG", "@{xG}"),
]
plotter = Plotter_Step_Goals_and_xG()
plotter.set_player("data/berterame_wyscout.csv", "Germán Berterame")
script, div = plotter.plot_step_goals_and_xG(TOOLTIPS)
plotter.set_player("data/aguirre_wyscout.csv", "Rodrigo Aguirre")
script_ra, div_ra = plotter.plot_step_goals_and_xG(TOOLTIPS, color = "red")
plotter.set_player("data/janssen_wyscout.csv", "Vincent Janssen")
script_vj, div_vj = plotter.plot_step_goals_and_xG(TOOLTIPS, color = "green")
plotter.set_player("data/ibanez_wyscout.csv", "Nico Ibáñez")
script_ni, div_ni = plotter.plot_step_goals_and_xG(TOOLTIPS, color = "yellow")


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

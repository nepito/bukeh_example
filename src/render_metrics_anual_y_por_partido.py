from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.colors import RGB
from bokeh.models import Panel, Tabs
import pandas as pd
from xg_plots import add_line_two_sd, add_line_three_sd


equipos_rivales = ["Tapatío", "Tepatitlán", "Mineros", "Cancún", "Venados", "Pumas"]
possession = ["Cimarrones", "Rivales"]
colors = ["#718dbf", "#e84d60"]
TOOLTIPS = [
    ("Juego", "@{match}"),
    ("Sistema rival", "@{scheme_rival}"),
    ("Sistema Cimarrones", "@{scheme_team}"),
]
match = [
    "Cimarrones - Tapatío 2:1",
    "Cimarrones - Tepatitlán 2:0",
    "Mineros - Cimarrones 1:1",
    "Cimarrones - Cancún 0:1",
    "Cimarrones - Venados 1:1",
    "Pumas - Cimarrones 2:2",
]
data = {
    "rival_teams": equipos_rivales,
    "match": match,
    "Rivales": [34, 61, 36, 31, 49, 59],
    "Cimarrones": [66, 39, 64, 69, 51, 41],
    "scheme_rival": ["3-4-3", "4-2-3-1", "4-1-4-1", "4-5-1", "4-2-3-1", "3-4-3"],
    "scheme_team": ["4-3-1-2", "4-3-1-2", "4-3-1-2", "4-3-1-2", "3-4-1-2", "3-4-3"],
}
df_possiession = pd.DataFrame(data).sort_values(by=["Cimarrones"])
sorted_equipos_rivales = df_possiession["rival_teams"]
p = figure(
    y_range=sorted_equipos_rivales,
    height=250,
    title="Posesión en los partidos de los Cimarrones de Sonora",
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
)
p.title.text_font_size = "12pt"
data = ColumnDataSource(df_possiession)
p.hbar_stack(
    possession, y="rival_teams", height=0.9, color=colors, source=data, legend_label=possession
)
p.y_range.range_padding = 0.4
p.ygrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"
p.xaxis.axis_label = "Posesión (%)"
p.yaxis.axis_label = "Cimarrones vs"

script, div = components(p)


TOOLTIPS = [
    ("Media anual", "@{mean_metrics_mean}"),
    ("Partido actual", "@{this_match_mean}"),
]


def get_groups_and_source(path):
    metrics = pd.read_csv(path)
    metrics["max"] = metrics["values"] + 0.1
    group = metrics.groupby("metrics")
    source = ColumnDataSource(group)
    group = metrics[::-1]["metrics"]
    return group, source


path = "data/metrics_intervals_tlaxcala.csv"
group, source = get_groups_and_source(path)


def get_metrics_from_round_and_team(round, team, TOOLTIPS):
    p = figure(
        y_range=group,
        x_range=(-4, 4),
        width=500,
        height=550,
        toolbar_location=None,
        tools="hover",
        tooltips=TOOLTIPS,
        title=f"Métricas de Cimarrones de Sonora \n Jornada {round}: {team}",
    )
    p.title.text_font_size = "12pt"
    return p


tlaxcala_p = get_metrics_from_round_and_team(1, "Tlaxcala", TOOLTIPS)


def plot_annual_metrics(p, source):
    p.hbar(y="metrics", left="values_max", right="max_max", height=0.4, source=source)
    p.patch(
        [-1, -1, 1, 1],
        [0, len(group), len(group), 0],
        color=RGB(154, 205, 50, 0.2),
        line_width=0,
    )
    p = add_line_two_sd(p, -2)
    p = add_line_two_sd(p, 2)
    p = add_line_three_sd(p, -3)
    p = add_line_three_sd(p, 3)
    return p


tlaxcala_p = plot_annual_metrics(tlaxcala_p, source)


def setup_axis_style(p, titulo):
    p.xaxis.minor_tick_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_color = None
    tab = Panel(child=p, title=titulo)
    return tab


tab_tlaxcala = setup_axis_style(tlaxcala_p, "Tlaxcala")

path = "data/metrics_intervals_dorados.csv"
group, source = get_groups_and_source(path)
dorados_p = get_metrics_from_round_and_team(2, "Dorados", TOOLTIPS)
dorados_p = plot_annual_metrics(dorados_p, source)
tab_dorados = setup_axis_style(dorados_p, "Dorados")

path = "data/metrics_intervals_mineros.csv"
group, source = get_groups_and_source(path)
dorados_p = get_metrics_from_round_and_team(3, "Mineros", TOOLTIPS)
dorados_p = plot_annual_metrics(dorados_p, source)
tab_mineros = setup_axis_style(dorados_p, "Mineros")

p = Tabs(tabs=[tab_tlaxcala, tab_dorados, tab_mineros])
script_interval, div_interval = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("metricas_anual_y_por_partido.html").render(
    script=script,
    div=div,
    script_interval=script_interval,
    div_interval=div_interval,
)
print(rendered)

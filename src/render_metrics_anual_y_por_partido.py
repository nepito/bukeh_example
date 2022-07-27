import re
from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.colors import RGB
from bokeh.models import Panel, Tabs
import pandas as pd
from xg_plots import (
    add_line_two_sd,
    add_line_three_sd,
    add_horizontal_line,
    add_patch_color,
    indirect_metrics,
    add_patch_to_direct_metrics,
)


colors = ["#718dbf", "#e84d60"]
df_possiession = pd.read_csv("data/horizontal_bars.csv").sort_values(by=["Cimarrones"])
possession = [df_possiession.columns[3], "Rivales"]
TOOLTIPS = [
    ("Juego", "@{match}"),
    ("Sistema rival", "@{scheme_rival}"),
    (f"Sistema {df_possiession.columns[3]}", "@{scheme_team}"),
]
sorted_equipos_rivales = df_possiession["rival_teams"]
p = figure(
    y_range=sorted_equipos_rivales,
    height=250,
    title=f"Posesión en los partidos de los {df_possiession.columns[3]}",
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
p.yaxis.axis_label = f"{df_possiession.columns[3]} vs"

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
    p = add_patch_color(p, [1, 1, 2, 2], [0, 6, 6, 0], [255, 140, 0, 0.1])
    p = add_patch_color(p, [2, 2, 3, 3], [0, 6, 6, 0], [255, 140, 0, 0.3])
    p = add_patch_color(p, [-2, -2, -1, -1], [0, 6, 6, 0], [154, 205, 50, 0.1])
    p = add_patch_color(p, [-3, -3, -2, -2], [0, 6, 6, 0], [154, 205, 50, 0.3])
    p = add_patch_to_direct_metrics(p)
    p = add_line_two_sd(p, -2)
    p = add_line_two_sd(p, 2)
    p = add_line_three_sd(p, -3)
    p = add_line_three_sd(p, 3)
    p = add_horizontal_line(p, 6)
    p = add_horizontal_line(p, 9)
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

path = "data/metrics_intervals_alebrijes.csv"
group, source = get_groups_and_source(path)
dorados_p = get_metrics_from_round_and_team(4, "Alebrijes", TOOLTIPS)
dorados_p = plot_annual_metrics(dorados_p, source)
tab_alebrijes = setup_axis_style(dorados_p, "Alebrijes")

p = Tabs(tabs=[tab_tlaxcala, tab_dorados, tab_mineros, tab_alebrijes])
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

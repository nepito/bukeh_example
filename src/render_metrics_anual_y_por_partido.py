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
    Plotter_Intervals_From_Rivals,
)


colors = ["#718dbf", "#e84d60"]
df_possiession = pd.read_csv("data/output_morelia.csv")
team = df_possiession.columns[3]
df_possiession = df_possiession.sort_values(by=[team])
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


path = "data/metrics_intervals_last-five-matches.csv"
plotter = Plotter_Intervals_From_Rivals(path)
tabls = [plotter.plot_intervals(x + 1, TOOLTIPS) for x in range(5)]
p = Tabs(tabs=tabls)
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

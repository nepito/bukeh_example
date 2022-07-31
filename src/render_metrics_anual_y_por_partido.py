import re
from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Panel, Tabs
import pandas as pd
from xg_plots import (
    Plotter_Intervals_From_Rivals,
)


colors = ["#FFC300", "#DF0404"]
df_possiession = pd.read_csv("data/output_morelia.csv")
team = df_possiession.columns[3]
df_possiession = df_possiession.sort_values(by=[team])
primer_partido = list(df_possiession.match)[-1]
primer_partido = primer_partido.split(" ")
marcador = primer_partido.pop().replace(":", " a ")
primer_partido = " ".join(primer_partido).replace("-", "vs")
rival = list(df_possiession.rival_teams)[-1]
schema_rival = list(df_possiession.scheme_rival)[-1]
schema_team = list(df_possiession.scheme_team)[-1]
ultimo_partido = list(df_possiession.match)[0]
ultimo_partido = ultimo_partido.split(" ")
ultimo_marcador = ultimo_partido.pop().replace(":", " a ")
ultimo_partido = " ".join(ultimo_partido).replace("-", "vs")
ultimo_rival = list(df_possiession.rival_teams)[0]
menor_posesion = list(df_possiession[team])[0]
possession = [df_possiession.columns[3], "Rivales"]
TOOLTIPS = [
    ("Juego", "@{match}"),
    ("Sistema rival", "@{scheme_rival}"),
    (f"Sistema {df_possiession.columns[3]}", "@{scheme_team}"),
]
sorted_equipos_rivales = df_possiession["rival_teams"]
p = figure(
    y_range=sorted_equipos_rivales,
    height=350,
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


path = "data/metrics_intervals_last-five-matches_morelia.csv"
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
    team="Atlético Morelia",
    primer_partido=primer_partido,
    marcador=marcador,
    schema_rival=schema_rival,
    schema_team=schema_team,
    rival=rival,
    ultimo_partido=ultimo_partido,
    ultimo_marcador=ultimo_marcador,
    ultimo_rival=ultimo_rival,
    menor_posesion=menor_posesion,
)
print(rendered)

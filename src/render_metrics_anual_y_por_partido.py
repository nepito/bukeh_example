from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Tabs
import pandas as pd
from xg_plots import (
    render_all_report,
    get_info_to_write,
    Plotter_Intervals_From_Rivals,
    COLOR,
)


df_possiession = pd.read_csv("data/output_morelia.csv")
team = df_possiession.columns[3]
df_possiession = df_possiession.sort_values(by=[team])

info_to_write = get_info_to_write(df_possiession)
team = info_to_write["team"]


colors = COLOR["Morelia"]
possession = [team, "Rivales"]
TOOLTIPS = [
    ("Juego", "@{match}"),
    ("Sistema rival", "@{scheme_rival}"),
    (f"Sistema {team}", "@{scheme_team}"),
]
sorted_equipos_rivales = df_possiession["rival_teams"]
p = figure(
    y_range=sorted_equipos_rivales,
    height=350,
    title=f"Posesión en los partidos de los {team}",
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
p.yaxis.axis_label = f"{team} vs"

script, div = components(p)


TOOLTIPS = [
    ("Media anual", "@{mean_metrics_mean}"),
    ("Partido actual", "@{this_match_mean}"),
]


path = "data/metrics_intervals_morelia.csv"


def plot_intrvals_of_the_last_five_matches(path, team, TOOLTIPS):
    plotter = Plotter_Intervals_From_Rivals(path, team)
    tabls = [plotter.plot_intervals(x + 1, TOOLTIPS) for x in range(5)]
    p = Tabs(tabs=tabls)
    return components(p)


script_interval, div_interval = plot_intrvals_of_the_last_five_matches(path, team, TOOLTIPS)

render_all_report(script, div, script_interval, div_interval, info_to_write, "Morelia")

from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import pandas as pd


equipos_rivales = ["Tepatitlán", "Mineros", "Cancún", "Venados", "Tapatio", "Pumas"]
possession = ["possession_team", "possession_rival"]
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
    "possession_rival": [34, 61, 36, 31, 49, 59],
    "possession_team": [66, 39, 64, 69, 51, 41],
    "scheme_rival": ["3-4-3", "4-2-3-1", "4-1-4-1", "4-5-1", "4-2-3-1", "3-4-3"],
    "scheme_team": ["4-3-1-2", "4-3-1-2", "4-3-1-2", "4-3-1-2", "3-4-1-2", "3-4-3"],
}
df_possiession = pd.DataFrame(data)
sorted_equipos_rivales = df_possiession.sort_values(by=["possession_team"])["rival_teams"]
p = figure(
    y_range=sorted_equipos_rivales,
    height=250,
    title="Posesión en los partidos de los Cimarrones de Sonora",
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
)
data = ColumnDataSource(df_possiession.sort_values(by=["possession_team"]))
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
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(
    script=script,
    div=div,
)
print(rendered)

from jinja2 import Environment, FileSystemLoader
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL, Span

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"

players = pd.read_csv("/workdir/data/femenil_player_for_scatter.csv")
source = ColumnDataSource(data=players)

TOOLTIPS = [
    ("Jugador", "@{player}"),
    ("Equipo", "@{team}"),
    ("Goles sin penales", "@{non_penalty_goals}"),
    ("Asistencias", "@{assists}"),
]

p = figure(
    title="Goles vs Asistencias",
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
    sizing_mode = "scale_both",
    aspect_ratio = 1,
)

median = players.median()
p.circle(x="goals_per_90", y="assists_per_90", radius="radio", color = "pink", source=source)
hline = Span(
    location=median["assists_per_90"],
    dimension="width",
    line_color="green",
    line_width=2,
    line_dash="dashed",
)
vline = Span(
    location=median["goals_per_90"],
    dimension="height",
    line_color="green",
    line_width=2,
    line_dash="dashed",
)

height = 0.04
image3 = ImageURL(
    url=dict(value=url), x=0.81, y=0.4, h=height, w=3.95 * height, anchor="bottom_left"
)
p.add_glyph(source, image3)
p.xaxis.axis_label = "Goles por cada 90 minutos"
p.yaxis.axis_label = "Asistencias por cada 90 minutos"
p.renderers.extend([hline, vline])
script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("xa_and_xg_players.html").render(
    script=script,
    div=div,
)
print(rendered)

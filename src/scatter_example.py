from jinja2 import Environment, FileSystemLoader
import pandas as pd


from bokeh.embed import components

from bokeh.plotting import figure

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ImageURL

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"
# create a Python dict as the basis of your ColumnDataSource

players = pd.read_csv("/workdir/data/player_for_scatter.csv")
# create a ColumnDataSource by passing the dict
source = ColumnDataSource(data=players)

# create a plot using the ColumnDataSource's two columns
p = figure(title="Goles vs Asistencias")

p.scatter(x="goals_per_90", y="assists_per_90", source=source)

image3 = ImageURL(url=dict(value=url), x=0.6, y=0.34, h=0.03, w=0.15, anchor="bottom_left")
p.add_glyph(source, image3)
p.xaxis.axis_label = "Goles por cada 90 minutos"
p.yaxis.axis_label = "Asistencias por cada 90 minutos"

script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(
    script=script,
    div=div,
)
print(rendered)

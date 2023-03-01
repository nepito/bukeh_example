from jinja2 import Environment, FileSystemLoader


from bokeh.embed import components

from bokeh.models import Panel, Tabs
from bokeh.plotting import figure

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Grid, ImageURL

url = "https://raw.githubusercontent.com/nepito/calculator-trs/develop/tests/data/logo_nies.png"
# create a Python dict as the basis of your ColumnDataSource
data = {"x_values": [1, 2, 3, 4, 5], "y_values": [6, 7, 2, 3, 6]}

# create a ColumnDataSource by passing the dict
source = ColumnDataSource(data=data)

# create a plot using the ColumnDataSource's two columns
p = figure(title="Goles vs Asistencias")

p.scatter(x="x_values", y="y_values", source=source)

image3 = ImageURL(url=dict(value=url), x=0, y=0, h=0.5, w=1, anchor="bottom_left")
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

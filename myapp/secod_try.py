from bokeh.models import Label, Title, NumeralTickFormatter
from bokeh.plotting import ColumnDataSource, figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.io import save
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pandas as pd

trimestre = pd.read_csv("trimestre_por_estudios.csv")
source = ColumnDataSource(trimestre)

TOOLS = "hover,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

TOOLTIPS = [("Horas semanales de trabajo", "@horas{0.}"), ("Ingreso", "@ingreso{($ 0,0)}")]
p = figure(tools=TOOLS, tooltips=TOOLTIPS, title="Ingresos por años de estudio")

p.scatter(x="anios_esc", y="ingreso", fill_alpha=0.6, hover_color="red", source=source)
p.xaxis.axis_label = "Años de estudios"
p.yaxis.axis_label = "Ingresos"
p.yaxis[0].formatter = NumeralTickFormatter(format="$0")

script, div = components(p)
fileLoader = FileSystemLoader("myapp")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(script=script, div=div)
print(rendered)

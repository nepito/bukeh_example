from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.io import save
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pandas as pd

trimestre = pd.read_csv("trimestre_por_estudios.csv")
x = trimestre["anios_esc"].values
y = trimestre["ingreso"].values
radii = trimestre["horas"].values

TOOLS = "hover,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"
TOOLTIPS = [
    ("Horas", "$radii"),
    ("Ingreso","$ingreso")
]
p = figure(tools=TOOLS, tooltips=TOOLTIPS, title="Ingresos por años de estudio")

p.scatter( x = x, y = y, radius=radii/40, fill_alpha=0.6, hover_color="red")
p.xaxis.axis_label = 'Años de estudios'
p.yaxis.axis_label = 'Ingresos'

script, div = components(p)
fileLoader = FileSystemLoader("myapp")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(script=script, div=div)
print(rendered)

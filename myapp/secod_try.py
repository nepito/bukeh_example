from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.io import save
import numpy as np
from jinja2 import Environment, FileSystemLoader

N = 4000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = np.array([[r, g, 150] for r, g in zip(50 + 2 * x, 30 + 2 * y)], dtype="uint8")

TOOLS = "hover,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

p = figure(tools=TOOLS)

p.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)


html = file_html(p, CDN, "my_plot.html")
save(p, "my_plot.html")
script, div = components(p)
fileLoader = FileSystemLoader("myapp")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(script=script, div=div)
print(rendered)

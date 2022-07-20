from bokeh.embed import components
import numpy as np
from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet

num_vars = 9

centre = 0.5

theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
# rotate theta such that the first axis is at the top
theta += np.pi / 2


def unit_poly_verts(theta, centre):
    """Return vertices of polygon for subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [centre] * 3
    verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
    return verts


def radar_patch(r, theta, centre):
    """Returns the x and y coordinates corresponding to the magnitudes of
    each variable displayed in the radar plot
    """
    # offset from centre of circle
    offset = 0.01
    yt = (r * centre + offset) * np.sin(theta) + centre
    xt = (r * centre + offset) * np.cos(theta) + centre
    return xt, yt


verts = unit_poly_verts(theta, centre)
x = [v[0] for v in verts]
y = [v[1] for v in verts]

p = figure(title="Baseline - Radar plot")
text = ["Sulfate", "Nitrate", "EC", "OC1", "OC2", "OC3", "OP", "CO", "O3", ""]
source = ColumnDataSource({"x": x + [centre], "y": y + [1], "text": text})

p.line(x="x", y="y", source=source)

labels = LabelSet(x="x", y="y", text="text", source=source)

p.add_layout(labels)

# example factor:
f1 = np.array([0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00])
f2 = np.array([0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00])
f3 = np.array([0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00])
f4 = np.array([0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00])
f5 = np.array([0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00])
# xt = np.array(x)
flist = [f1, f2, f3, f4, f5]
colors = ["blue", "green", "red", "orange", "purple"]
for i in range(len(flist)):
    xt, yt = radar_patch(flist[i], theta, centre)
    p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])
show(p)

script, div = components(p)
fileLoader = FileSystemLoader("myapp")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(script=script, div=div)
print(rendered)

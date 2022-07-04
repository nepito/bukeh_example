from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.sampledata.sprint import sprint
from bokeh.colors import RGB
import pandas as pd


metrics = pd.read_csv("data/metrics_intervals.csv")
metrics["max"] = metrics["values"]+0.1
sprint.Year = sprint.Year.astype(str)
group = metrics.groupby("metrics")
source = ColumnDataSource(group)

p = figure(
    y_range=group,
    x_range=(-4, 4),
    width=400,
    height=550,
    toolbar_location=None,
    title="Time spreads for sprint medalists (by year)",
)
p.hbar(y="metrics", left="values_max", right="max_max", height=0.4, source=source)
p.patch(
    [-1, -1, 1, 1],
    [0, len(group), len(group), 0],
    color=RGB(154,205,50, 0.2),
    line_width=0,
)

p.patch(
    [-2, -2, -1, -1],
    [0, len(group), len(group), 0],
    color=RGB(255,140,0, 0.2),
    line_width=0,
)

p.patch(
    [1, 1, 2, 2],
    [0, len(group), len(group), 0],
    color=RGB(255,140,0, 0.2),
    line_width=0,
)

p.patch(
    [-3, -3, -2, -2],
    [0, len(group), len(group), 0],
    color=RGB(255,69,0, 0.2),
    line_width=0,
)

p.patch(
    [2, 2, 3, 3],
    [0, len(group), len(group), 0],
    color=RGB(255,69,0, 0.2),
    line_width=0,
)

p.ygrid.grid_line_color = None
p.xaxis.axis_label = "Time (seconds)"
p.outline_line_color = None

script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(
    script=script,
    div=div,
)
print(rendered)

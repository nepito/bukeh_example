from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Span
from bokeh.sampledata.sprint import sprint
from bokeh.colors import RGB
import pandas as pd

TOOLTIPS = [
    ("Media anual", "@{mean_metrics_mean}"),
    ("Partido actual", "@{this_match_mean}"),
]

metrics = pd.read_csv("data/metrics_intervals.csv")
metrics["max"] = metrics["values"] + 0.1
sprint.Year = sprint.Year.astype(str)
group = metrics.groupby("metrics")
source = ColumnDataSource(group)

p = figure(
    y_range=group,
    x_range=(-4, 4),
    width=400,
    height=550,
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
    title="Métricas de Cimarrones de Sonora \n Jornada 1: Tlaxcala",
)
p.hbar(y="metrics", left="values_max", right="max_max", height=0.4, source=source)
p.patch(
    [-1, -1, 1, 1],
    [0, len(group), len(group), 0],
    color=RGB(154, 205, 50, 0.2),
    line_width=0,
)

first_line = Span(
    location=-2, dimension='height', line_color=RGB(255, 140, 0, 0.2),
    line_dash='dashed', line_width=3)

p.add_layout(first_line)

first_line = Span(
    location=2, dimension='height', line_color=RGB(255, 140, 0, 0.2),
    line_dash='dashed', line_width=3)

p.add_layout(first_line)

second_line = Span(
    location=-3, dimension='height', line_color=RGB(255, 69, 0),
    line_dash='dashed', line_width=3)

p.add_layout(second_line)

second_line = Span(
    location=3, dimension='height', line_color=RGB(255, 69, 0),
    line_dash='dashed', line_width=3)

p.add_layout(second_line)

p.ygrid.grid_line_color = None
p.outline_line_color = None

script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(
    script=script,
    div=div,
)
print(rendered)

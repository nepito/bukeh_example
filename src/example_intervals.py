from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.sampledata.sprint import sprint
from bokeh.colors import RGB
from bokeh.models import Panel, Tabs
import pandas as pd
from xg_plots import add_line_two_sd, add_line_three_sd

TOOLTIPS = [
    ("Media anual", "@{mean_metrics_mean}"),
    ("Partido actual", "@{this_match_mean}"),
]

metrics = pd.read_csv("data/metrics_intervals_tlaxcala.csv")
metrics["max"] = metrics["values"] + 0.1
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


p = add_line_two_sd(p, -2)
p = add_line_two_sd(p, 2)
p = add_line_three_sd(p, -3)
p = add_line_three_sd(p, 3)

p.xaxis.minor_tick_line_color = None
p.ygrid.grid_line_color = None
p.outline_line_color = None
tab_tlaxcala = Panel(child=p, title="tlaxcala")


metrics = pd.read_csv("data/metrics_intervals_dorados.csv")
metrics["max"] = metrics["values"] + 0.1
group = metrics.groupby("metrics")
source = ColumnDataSource(group)

p_d = figure(
    y_range=group,
    x_range=(-4, 4),
    width=400,
    height=550,
    toolbar_location=None,
    tools="hover",
    tooltips=TOOLTIPS,
    title="Métricas de Cimarrones de Sonora \n Jornada 2: Dorados",
)
p_d.hbar(y="metrics", left="values_max", right="max_max", height=0.4, source=source)
p_d.patch(
    [-1, -1, 1, 1],
    [0, len(group), len(group), 0],
    color=RGB(154, 205, 50, 0.2),
    line_width=0,
)


p_d = add_line_two_sd(p_d, -2)
p_d = add_line_two_sd(p_d, 2)
p_d = add_line_three_sd(p_d, -3)
p_d = add_line_three_sd(p_d, 3)

p_d.xaxis.minor_tick_line_color = None
p_d.ygrid.grid_line_color = None
p_d.outline_line_color = None
tab_dorados = Panel(child=p_d, title="dorados")

p = Tabs(tabs=[tab_tlaxcala, tab_dorados])
script, div = components(p)
fileLoader = FileSystemLoader("reports")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(
    script=script,
    div=div,
)
print(rendered)

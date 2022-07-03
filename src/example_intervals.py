from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.sampledata.sprint import sprint
from bokeh.colors import RGB


sprint.Year = sprint.Year.astype(str)
group = sprint.groupby("Year")
source = ColumnDataSource(group)

p = figure(
    y_range=group,
    x_range=(9.5, 12.7),
    width=400,
    height=550,
    toolbar_location=None,
    title="Time spreads for sprint medalists (by year)",
)
p.hbar(y="Year", left="Time_min", right="Time_max", height=0.4, source=source)
p.patch(
    [10.5, 10.5, 11.5, 11.5],
    [0, len(group), len(group), 0],
    color=RGB(255, 99, 132, 0.2),
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

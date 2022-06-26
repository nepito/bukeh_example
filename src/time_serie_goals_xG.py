import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.colors import RGB
from jinja2 import Environment, FileSystemLoader

def get_player(path, name):
    player = pd.read_csv(path)
    selected_columns = ["Date","Goals","xG", "Match", "Minutes played"]
    just_mx = player["Competition"] == "Mexico. Liga MX"
    cleaned_player = player[just_mx][selected_columns]
    cleaned_player["player"] = name
    cleaned_player["Date"] = pd.to_datetime(cleaned_player["Date"])
    return cleaned_player

berterame = get_player("data/berterame_wyscout.csv", "Germán Berterame")
aguirre = get_player("data/aguirre_wyscout.csv", "Rodrigo Aguirre")
TOOLTIPS = [
    ("Partido", "@{Match}"),
    ("Minutos Jugados", "@{Minutes played}"),
    ("xG", "@{xG}"),
]
data = ColumnDataSource(berterame)
data2 = ColumnDataSource(aguirre)
plot = figure(x_axis_type='datetime',
              title='Goles en la Liga MX',
             x_axis_label = "Date",
              y_axis_label = "Goles",
	      tooltips=TOOLTIPS)
plot.step(x='Date', y = 'Goals', source = data, color = 'blue')
plot.line(x='Date', y = 'Goals', source = data, color = RGB(54, 162, 235, 0.0))
plot.step(x='Date', y = 'Goals', source = data2, color = 'red')
plot.line(x='Date', y = 'Goals', source = data2, color = RGB(255, 99, 132, 0.2))
show(plot)

script, div = components(plot)
fileLoader = FileSystemLoader("myapp")
env = Environment(loader=fileLoader)

rendered = env.get_template("template.html").render(script=script, div=div)
print(rendered)
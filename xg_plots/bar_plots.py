from jinja2 import Environment, FileSystemLoader
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Tabs
from xg_plots import COLOR, COLOR_IN_TEXT, Plotter_Intervals_From_Rivals


def get_match(df_possiession, match):
    team = df_possiession.columns[3]
    df_possiession = df_possiession.sort_values(by=[team])
    primer_partido = list(df_possiession.match)[match]
    primer_partido = primer_partido.split(" ")
    marcador = primer_partido.pop().replace(":", " a ")
    return " ".join(primer_partido).replace("-", "vs"), marcador


def get_bar_plot_of_possession(df_possiession, team):
    colors = COLOR[team]
    possession = [df_possiession.columns[3], "Rivales"]
    TOOLTIPS = [
        ("Juego", "@{match}"),
        ("Sistema rival", "@{scheme_rival}"),
        (f"Sistema {df_possiession.columns[3]}", "@{scheme_team}"),
    ]
    sorted_equipos_rivales = df_possiession["rival_teams"]
    p = figure(
        y_range=sorted_equipos_rivales,
        height=350,
        title=f"Posesión en los partidos de los {df_possiession.columns[3]}",
        toolbar_location=None,
        tools="hover",
        tooltips=TOOLTIPS,
    )
    p.title.text_font_size = "12pt"
    data = ColumnDataSource(df_possiession)
    p.hbar_stack(
        possession, y="rival_teams", height=0.9, color=colors, source=data, legend_label=possession
    )
    p.y_range.range_padding = 0.4
    p.ygrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.xaxis.axis_label = "Posesión (%)"
    p.yaxis.axis_label = f"{df_possiession.columns[3]} vs"
    return components(p)


def get_info_to_write(df_possiession):
    team = df_possiession.columns[3]
    primer_partido, marcador = get_match(df_possiession, match=-1)
    ultimo_partido, ultimo_marcador = get_match(df_possiession, match=0)
    info_to_write = dict(
        team=team,
        primer_partido=primer_partido,
        marcador=marcador,
        ultimo_partido=ultimo_partido,
        ultimo_marcador=ultimo_marcador,
        rival=list(df_possiession.rival_teams)[-1],
        schema_rival=list(df_possiession.scheme_rival)[-1],
        schema_team=list(df_possiession.scheme_team)[-1],
        ultimo_rival=list(df_possiession.rival_teams)[0],
        menor_posesion=list(df_possiession[team])[0],
    )
    return info_to_write


def render_all_report(script, div, script_interval, div_interval, info_to_write, team):
    fileLoader = FileSystemLoader("reports")
    env = Environment(loader=fileLoader)
    rendered = env.get_template("metricas_anual_y_por_partido.html").render(
        script=script,
        div=div,
        script_interval=script_interval,
        div_interval=div_interval,
        team=info_to_write["team"],
        primer_partido=info_to_write["primer_partido"],
        marcador=info_to_write["marcador"],
        schema_rival=info_to_write["schema_rival"],
        schema_team=info_to_write["schema_team"],
        rival=info_to_write["rival"],
        ultimo_partido=info_to_write["ultimo_partido"],
        ultimo_marcador=info_to_write["ultimo_marcador"],
        ultimo_rival=info_to_write["ultimo_rival"],
        menor_posesion=info_to_write["menor_posesion"],
        color=COLOR_IN_TEXT[team],
    )
    print(rendered)


def plot_intrvals_of_the_last_five_matches(path, team):
    TOOLTIPS = [
        ("Media anual", "@{mean_metrics_mean}"),
        ("Partido actual", "@{this_match_mean}"),
    ]
    plotter = Plotter_Intervals_From_Rivals(path, team)
    tabls = [plotter.plot_intervals(x + 1, TOOLTIPS) for x in range(5)]
    p = Tabs(tabs=tabls)
    return components(p)

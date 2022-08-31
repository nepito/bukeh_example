import pandas as pd
from bokeh.embed import components
from xg_plots import (
    render_all_report,
    get_info_to_write,
    get_bar_plot_of_possession,
    plot_intrvals_of_the_last_five_matches,
)
import typer


app = typer.Typer(help="Awesome CLI user manager.")


@app.command()
def write_report_abot_teams(path_possession="", path_intervals="", color_team=""):
    df_possiession = pd.read_csv(path_possession)
    team = df_possiession.columns[3]
    df_possiession = df_possiession.sort_values(by=[team])
    info_to_write = get_info_to_write(df_possiession)
    team = info_to_write["team"]
    p = get_bar_plot_of_possession(df_possiession, color_team)
    script, div = components(p)
    script_interval, div_interval = plot_intrvals_of_the_last_five_matches(path_intervals, team)
    render_all_report(script, div, script_interval, div_interval, info_to_write, color_team)


if __name__ == "__main__":
    app()

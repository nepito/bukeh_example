import hashlib
import os
import xg_plots as xgp
import pytest
import pandas as pd


def test_return_one():
    expected = 1
    obtained = xgp.return_one()
    assert expected == obtained


@pytest.mark.xfail
def test_example_bar_plots():
    set_up_tests()
    os.system("python src/example_bar_plots.py > salidita.html")
    obtained_hash = hashlib.md5(open("salidita.html", "rb").read()).hexdigest()
    expected_hash = "20b7936e4e1e4bd9190cf824fda4847d"
    assert expected_hash == obtained_hash


@pytest.mark.xfail
def test_example_intervals():
    set_up_tests()
    os.system("python src/example_intervals.py > salidita.html")
    obtained_hash = hashlib.md5(open("salidita.html", "rb").read()).hexdigest()
    expected_hash = "20b7936e4e1e4bd9190cf824fda4847d"
    assert expected_hash == obtained_hash


def set_up_tests():
    os.system("rm --force salidita.html")


df_possiession = pd.read_csv("tests/data/output_morelia.csv")


def test_get_match():
    expected_match = "Atlético Morelia vs Tapatío"
    obtained_match, result = xgp.get_match(df_possiession, -1)
    assert obtained_match == expected_match
    assert result == "1 a 2"
    expected_match = "Tlaxcala vs Atlético Morelia"
    obtained_match, _ = xgp.get_match(df_possiession, 0)
    assert obtained_match == expected_match


p = xgp.get_bar_plot_of_possession(df_possiession, team="Morelia")


def test_hover_tooltips():
    expected_tooltips = [
        ("Juego", "@{match}"),
        ("Sistema rival", "@{scheme_rival}"),
        ("Sistema Morelia", "@{scheme_team}"),
    ]
    obtained_tooltips = p.hover.tooltips
    assert obtained_tooltips == expected_tooltips


def test_legend():
    assert p.legend.location == "top_left"
    assert p.legend.orientation == "horizontal"


def test_misc_of_figure():
    assert p.title.text_font_size == "12pt"
    assert p.y_range.range_padding == 0.4
    assert p.ygrid.grid_line_color is None
    assert p.outline_line_color is None
    assert p.xaxis.axis_label == "Posesión (%)"
    assert p.yaxis.axis_label == "Morelia vs"
    assert p.title.text == "Posesión en los partidos de los Morelia"
    assert p.plot_height == 350
    assert p.toolbar_location is None
    expected_rivals_teams = [
        "Pumas",
        "Venados",
        "Tepatitlán",
        "Universidad",
        "Atlante",
        "Tampico",
        "Celaya",
        "Dorados",
        "Cancún",
        "Correcaminos",
        "Tapatío",
        "Alebrijes",
        "Cimarrones",
        "Raya2",
        "Mineros",
        "Tlaxcala",
    ]
    assert p.y_range.factors == expected_rivals_teams
    assert p.renderers[0].glyph.fill_color == "#FFC300"
    assert p.renderers[1].glyph.fill_color == "#DF0404"
    assert p.renderers[1].glyph.height == 0.9
    assert p.legend.items[1].label["value"] == "Rivales"


def test_misc_intervals():
    TOOLTIPS = [
        ("Media anual", "@{mean_metrics_mean}"),
        ("Partido actual", "@{this_match_mean}"),
    ]
    path = "tests/data/metrics_intervals_morelia.csv"
    plotter = xgp.Plotter_Intervals_From_Rivals(path, "Morelia")
    panel = plotter.plot_intervals(1, TOOLTIPS)
    figura = panel.child
    assert TOOLTIPS == figura.hover.tooltips
    assert figura.title.text == "Métricas de Morelia \n Jornada 1: Tlaxcala"
    metrics = [
        "PDA",
        "Distancia de los disparos",
        "Pérdidas altas",
        "Pérdidas medias",
        "Pérdidas bajas",
        "Disparos en contra",
        "Contra ataque",
        "Pases por posesión",
        "Posesión",
        "Recuperación alta",
        "Recuperación media",
        "Recuparación baja",
        "xG",
    ]
    assert figura.y_range.factors == metrics


def test_get_info_to_write():
    info_to_write = xgp.get_info_to_write(df_possiession)
    assert info_to_write["primer_partido"] == "Atlético Morelia vs Tapatío"
    assert info_to_write["marcador"] == "1 a 2"
    assert info_to_write["ultimo_partido"] == "Tlaxcala vs Atlético Morelia"
    assert info_to_write["ultimo_marcador"] == "0 a 4"
    assert info_to_write["ultimo_rival"] == "Pumas"
    assert info_to_write["rival"] == "Tlaxcala"

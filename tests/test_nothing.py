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
    obtained_match = xgp.get_match(df_possiession, -1)
    assert obtained_match == expected_match

def test_hover_tooltips():
    expected_tooltips = [('Juego', '@{match}'), ('Sistema rival', '@{scheme_rival}'), ('Sistema Morelia', '@{scheme_team}')]
    obtained_tooltips = p.hover.tooltips
    assert obtained_tooltips == expected_tooltips
import hashlib
import os
import xg_plots as xgp


def test_return_one():
    expected = 1
    obtained = xgp.return_one()
    assert expected == obtained


def test_example_bar_plots():
    os.system('python src/example_bar_plots.py > salidita.html')
    obtained_hash = hashlib.md5(open('salidita.html','rb').read()).hexdigest()
    expected_hash = "931ff61ed21857e2121b99e85186051d"
    assert expected_hash == obtained_hash
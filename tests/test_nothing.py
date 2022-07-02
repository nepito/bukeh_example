import xg_plots as xgp

def test_return_one():
    expected = 1
    obtained = xgp.return_one()
    assert expected == obtained
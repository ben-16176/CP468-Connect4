from c4.gui import column_from_x


def test_column_from_x_maps_clicks_to_columns():
    assert column_from_x(40, 80, 7) == 0
    assert column_from_x(120, 80, 7) == 1
    assert column_from_x(200, 80, 7) == 2
    assert column_from_x(9999, 80, 7) is None

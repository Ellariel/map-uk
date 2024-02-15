from __future__ import annotations

import pandas as pd

from map_uk import ChoroplethMapUK, constants

data = pd.read_csv(constants.Paths.DATA_DIR / "data.csv")

m = ChoroplethMapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    legend_name="Median earnings (£)",
)
m.save(constants.Paths.STATIC_DIR / "map1_basic.html")

m = ChoroplethMapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    legend_name="Median earnings (£)",
    fill_color="viridis",
    use_jenks=True,
)
m.save(constants.Paths.STATIC_DIR / "map2_basic.html")

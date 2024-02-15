from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from map_uk import ChoroplethMapUK
from tests.utils import run_within_dir

if TYPE_CHECKING:
    from pathlib import Path


def test_choropleth(tmp_path: Path) -> None:
    """Testing ChoroplethMapUK function."""
    with run_within_dir(tmp_path):
        # Example usage
        data = pd.DataFrame(
            {"geocode": ["E07000207", "E07000142"], "Median": [100, 200]}
        )
        m = ChoroplethMapUK(geojson_simplify_tolerance=0.0001).plot(
            data,
            geocode_column="mnemonic",
            value_column_name="Median",
            legend_name="Testing ChoroplethMapUK",
        )
        m.save("map.html")
        assert m

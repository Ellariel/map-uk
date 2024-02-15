from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from map_uk import MapUK
from tests.utils import run_within_dir

if TYPE_CHECKING:
    from pathlib import Path


def test_plot(tmp_path: Path) -> None:
    """."""
    with run_within_dir(tmp_path):

        def get_color(value: int) -> None:
            """."""
            if not value:
                return "grey"
            if value > 150:  # noqa: PLR2004
                return "green"
            else:
                return "blue"

        def style(feature) -> None:
            """."""
            return {"fillColor": get_color(feature.get("properties").get("Median"))}

        # Example usage
        data = pd.DataFrame(
            {"geocode": ["E07000207", "E07000142"], "Median": [100, 200]}
        )

        m = MapUK(geojson_simplify_tolerance=0.0001).plot(
            data,
            geocode_column="mnemonic",
            value_column_name="Median",
            style_function=style,
            legend_name="Testing MapUK"
        )
        m.save("map.html")

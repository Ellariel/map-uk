from __future__ import annotations

import folium
import pandas as pd

from map_uk import MapUK, constants


def get_color(value, limit):
    """Example function that specifies colour based on condition."""
    if not value:
        return "grey"
    if value > limit:
        return "green"
    else:
        return "blue"


def style(feature):
    """Example function that specifies colour style to be used in folium map."""
    return {
        "fillColor": get_color(feature.get("properties").get("Median"), limit=35000)
    }


data = pd.read_csv(constants.Paths.DATA_DIR / "data.csv")

m = MapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    style_function=style,
    name="Median earnings (£) value",
)

m.save(constants.Paths.STATIC_DIR / "map3_custom.html")


tooltip = folium.GeoJsonTooltip(
    fields=["geocode", "ename", "Median"],
    aliases=["Geography Code:", "Example Full Name:", "Median Earnings:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 3px solid black;
        border-radius: 10px;
        box-shadow: 10px;
    """,
    max_width=800,
)

m = MapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    style_function=style,
    name="Median earnings (£) value",
    tooltip=tooltip,
)

m.save(constants.Paths.STATIC_DIR / "map4_tooltip.html")

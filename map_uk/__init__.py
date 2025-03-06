from __future__ import annotations  # noqa: D104

from map_uk.map.choropleth import ChoroplethMapUK
from map_uk.map.map import MapUK

class Map(map_uk.ChoroplethMapUK):
    def __init__(self, **kwargs):
        super().__init__(data_dir=map_uk.constants.TOP_FOLDER / "map_uk", **kwargs)

__all__ = (
    "ChoroplethMapUK",
    "MapUK",
    "Map",
)

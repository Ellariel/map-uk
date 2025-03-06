from __future__ import annotations  # noqa: D104

from map_uk.map.choropleth import ChoroplethMapUK
# from map_uk.map.map import MapUK
from map_uk.constants import TOP_FOLDER 

class MapUK(ChoroplethMapUK):
    def __init__(self, **kwargs):
        super().__init__(data_dir=TOP_FOLDER / "map_uk", **kwargs)

__all__ = (
    "ChoroplethMapUK",
    "MapUK",
)

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import folium

from map_uk.constants import DEFAULT_MAP_ARGS, Paths
from map_uk.geojson.getter import GeoJsonGetter

if TYPE_CHECKING:
    from pathlib import Path

    import pandas as pd


class BaseMapUK(ABC):
    """Abstract base class for creating maps of the UK using Folium.

    This class provides basic functionalities for downloading and handling GeoJSON data,
    initializing a Folium map, and defining an abstract method for plotting.
    """

    def __init__(
        self,
        url: str = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_May_2023_UK_BGC_V2/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson",
        data_dir: Path = Paths.DATA_DIR,
        geojson_simplify_tolerance: float | None = None,
        **kwargs: dict,
    ) -> None:
        """Args.

        url (str, optional): URL to download the GeoJSON file. Defaults to the Local Authority Districts 2023 data, 20m simplified.
        data_dir (Path, optional): Directory to save the downloaded GeoJSON file. Defaults to Paths.DATA_DIR.
        geojson_simplify_tolerance (float | None, optional): Tolerance level for GeoJSON simplification.
            If None, no simplification is performed. Lower values lead to simpler maps. Sensible values for
            coordinates stored in degrees are in the range of 0.0001 to 10. Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the folium.Map() function. By default, only `location`
            and `zoom_start` are passed with default values.
        """
        self.geojson_simplify_tolerance = geojson_simplify_tolerance
        self.geojson_path = data_dir / "lad-2023.geojson"
        self.url = url

        map_args = {**DEFAULT_MAP_ARGS, **kwargs}
        self.m = folium.Map(**map_args)

    @abstractmethod
    def plot(
        self,
        df: pd.DataFrame,
        value_column_name: str,
        geocode_column: str,
        **kwargs: Any,
    ) -> folium.Map:
        """."""
        raise NotImplementedError

    def _get_geojson(self) -> dict:
        """Retrieves the GeoJSON data for the map.

        Downloads the GeoJSON file if it does not exist locally and optionally simplifies it.

        Returns:
            dict: The contents of the GeoJSON file, either in its original or simplified form.
        """
        return GeoJsonGetter(
            url=self.url,
            geojson_path=self.geojson_path,
            geojson_simplify_tolerance=self.geojson_simplify_tolerance,
        ).get()

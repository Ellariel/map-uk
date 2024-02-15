from __future__ import annotations

from typing import TYPE_CHECKING

import folium
import geopandas as gpd

from map_uk.map.base import BaseMapUK

if TYPE_CHECKING:
    import pandas as pd


class MapUK(BaseMapUK):
    """A class for creating custom maps of the UK using `folium.GeoJson`."""

    def plot(
        self,
        df: pd.DataFrame,
        value_column_name: str,
        geocode_column: str,
        **kwargs: dict,
    ) -> folium.Map:
        """Creates and adds a custom map layer to the Folium map instance.

        This method processes the input DataFrame and GeoJSON data to create a
        Folium GeoJson layer, which is then added to the map.

        Args:
            df (pd.DataFrame): DataFrame containing the data for the map.
            value_column_name (str): Name of the column in df that contains the values to be visualized.
            geocode_column (str): Name of the column in df that contains the geography area codes.
            **kwargs: Additional keyword arguments to customize the GeoJson layer.

        Returns:
            folium.Map: The Folium Map object with the custom layer added.
        """
        geography_df = self._prepare_input_data(df, geocode_column)
        geography_geojson = self._get_geojson()
        geography_geojson = self._add_values_to_geojson(geography_geojson, geography_df)
        tooltip = self._get_default_tooltip(value_column_name)

        default_args = {
            "weight": 1,
            "opacity": 1,
            "color": "black",
            "dashArray": "3",
            "fillOpacity": 0.7,
            "tooltip": tooltip,
        }

        plot_args = {**default_args, **kwargs}
        folium.GeoJson(geography_geojson, **plot_args).add_to(self.m)

        folium.LayerControl().add_to(self.m)

        return self.m

    @staticmethod
    def _prepare_input_data(df: pd.DataFrame, geocode_column: str) -> pd.DataFrame:
        geography_df = df.rename(columns={geocode_column: "geocode"})
        geography_df["geocode"] = geography_df["geocode"].astype("str")
        return geography_df

    @staticmethod
    def _add_values_to_geojson(geojson: dict, df: pd.DataFrame) -> dict:
        gdf = gpd.GeoDataFrame.from_features(geojson["features"])
        gdf = gdf.rename(columns={"LADCD23": "geocode", "LADNM23": "ename"})
        merged_gdf = gdf.merge(df, on="geocode", how="left")
        return merged_gdf.to_json()

    @staticmethod
    def _get_default_tooltip(value_column_name: str) -> folium.GeoJsonTooltip:
        return folium.GeoJsonTooltip(
            fields=["geocode", "ename", value_column_name],
            aliases=["Geocode:", "Name:", f"{value_column_name}:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )

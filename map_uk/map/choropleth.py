from __future__ import annotations

from typing import TYPE_CHECKING

import folium

from map_uk.map.base import BaseMapUK

if TYPE_CHECKING:
    import pandas as pd

class ChoroplethMapUK(BaseMapUK):
    """A class for creating Choropleth maps of the UK using `folium.Choropleth`."""

    def plot(
        self,
        df: pd.DataFrame,
        value_column_name: str,
        geocode_column: str,
        **kwargs: dict,
    ) -> folium.Map:
        """Take a pandas DataFrame with UK geographical data and plot a Choropleth map based on the data.

        Any **kwargs are passed on to `folium.Choropleth`. For example, to change the fill color, run

        ```
        kwargs = {"fill_opacity": 1}
        m = ChoroplethMapUK(...).plot(..., **kwargs)
        ```

        Args:
            df (pd.DataFrame): DataFrame containing the data for the Choropleth map.
            value_column_name (str): Name of the column in df that contains the values to be visualized.
            geocode_column (str): Name of the column in df that contains the relevant geography code.
            tooltip (bool): Add a simple tooltip.
            **kwargs: Additional keyword arguments that are passed to `folium.Choropleth`.

        Returns:
            folium.Map: The Folium Map object with the Choropleth layer added.
        """
        geography_geojson = self._get_geojson()

        default_args = {
            "geo_data": geography_geojson,
            "name": "choropleth",
            "data": df,
            "columns": [geocode_column, value_column_name],
            "key_on": "feature.properties.geocode",
            "fill_color": "GnBu",
            "fill_opacity": 0.8,
            "line_opacity": 0.2,
            "nan_fill_color": "white",
        }
        choropleth_args = {**default_args, **kwargs}

        choropleth = folium.Choropleth(**choropleth_args).add_to(self.m)

        self._add_tooltip(choropleth, df, geocode_column, value_column_name)

        folium.LayerControl().add_to(self.m)

        return self.m

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

    def _add_tooltip(
        self,
        choropleth: folium.Choropleth,
        df: pd.DataFrame,
        geocode_column: str,
        value_column_name: str,
    ) -> None:
        df_indexed = df.set_index(geocode_column)
        for s in choropleth.geojson.data["features"]:
            geocode = str(s.get("properties")["geocode"])
            if geocode in df_indexed.index:
                s["properties"][value_column_name] = str(
                    df_indexed.loc[geocode, value_column_name]
                )
            else:
                s["properties"][value_column_name] = None
        tooltip = self._get_default_tooltip(value_column_name)
        tooltip.add_to(choropleth.geojson)

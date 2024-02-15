# map-uk

_map-uk_ is a Python package to help you quickly create maps of UK geographies such as [Local Authority Districts](https://geoportal.statistics.gov.uk/maps/e8b361ba9e98418ba8ff2f892d00c352). The package will automatically download relevant `geojson` files so all that is required is a dataset with two columns: one containing your `geocode` and one with the relevant values to plot on a map. Data is shown on a map using [folium](https://github.com/python-visualization/folium).

Credit to [Florian Maas](https://github.com/fpgmaas) for the idea and initial codebase in their [map-nl](https://github.com/fpgmaas/map-nl/tree/main) package.

# Usage 
## Choropleth maps 

You can use `ChoroplethMapUK` to create quick choropleth maps of 2023 Local Authority Districts using the below: 
```python
import pandas as pd
from map_uk import ChoroplethMapUK, constants

data = pd.read_csv(constants.Paths.DATA_DIR / "data.csv")
m = ChoroplethMapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    legend_name="Median earnings (£)"
)
m.save(constants.Paths.STATIC_DIR / "map1_basic.html")
```

Other keyword-arguments passed to `plot()` are passed onto `folium.Choropleth`. For example, we can change the colour palette and use the Jenks Natural Breaks algorithm:

```python
m = ChoroplethMapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    legend_name="Median earnings (£)",
    fill_color="viridis",
    use_jenks=True,
)
m.save(constants.Paths.STATIC_DIR / "map2_basic.html")
```
## Custom maps
You can use `MapUK` to create custom LAD 2023 maps of the UK.  

```python
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
    return {"fillColor": get_color(feature.get("properties").get("Median"), limit=35000)}

data = pd.read_csv(constants.Paths.DATA_DIR / "data.csv")

m = MapUK().plot(
    data,
    geocode_column="mnemonic",
    value_column_name="Median",
    style_function=style,
    name="Median earnings (£) value",
)

m.save(constants.Paths.STATIC_DIR / "map3_custom.html")
```
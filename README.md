<p align="center" style="margin: 30px 30px 40px 30px;">
  <img alt="map uk" height="150" src="docs/static/uk.png?raw=true">
</p>

# map-uk

_map-uk_ is a Python package to help you quickly create maps of UK geographies such as [Local Authority Districts](https://geoportal.statistics.gov.uk/maps/e8b361ba9e98418ba8ff2f892d00c352). The package will automatically download relevant `geojson` files so all that is required is a dataset with two columns: one containing your `geocode` and one with the relevant values to plot on a map. Data is shown on a map using [folium](https://github.com/python-visualization/folium).

Currently only Local Authority Districta (2023) are supported, further development will allow users to specify the geography type they want plotting (e.g. specific year of Local Authority Districts, Lower Super Output Areas, Combined Authorities) and _map-uk_ will handle everything else. 

Credit to [Florian Maas](https://github.com/fpgmaas) for the idea and initial codebase from their [map-nl](https://github.com/fpgmaas/map-nl/tree/main) package.

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

The above example will colour any LADs with a median annual salary above 35000 green, blue if it is below 35000, and grey if no median value is found. 

As in `ChoroplethMapUK`, you can pass keyword arguments to the `plot()` function. For example, you can modify the default tooltip and define your own:
```python
tooltip = folium.GeoJsonTooltip(
    fields=["geocode", "ename", "Median"],
    aliases=["Geography Code:", "LAD Name:", "Median Earnings:"],
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
```

# Install
This assumes you have installed [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer).

First ensure you have a supported Python version installed on your machine:
```bash
pyenv install 3.10.*
```
Any supported version is `>=3.9,` and `<3.12`.

Set the local environment and install dependencies:

Note: you may get an error running the 'env use python' command. Instead, just try running poetry install
```bash
pyenv local 3.10.*
poetry env use python
poetry install
```

Finally, reload the window with `Cmd + R` (or via the command palette `Cmd + Shift + P` > `Developer: Reload window`), then activate the newly created virtual environment:

Note: if the command doesn't work, you can open the command palette, search 'python' and select 'Select Python interpreter' and choose the Poetry environment there - then reload the window.

```bash
source $(poetry env info --path)/bin/activate
```
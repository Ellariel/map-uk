from __future__ import annotations

from pathlib import Path

from map_uk.geojson.getter import GeoJsonGetter
from tests.utils import run_within_dir


def test_skip_download_when_file_exists(
    tmp_path: Path, uk_lad_geojson_sample: str
) -> None:
    """."""
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", uk_lad_geojson_sample)
        geojson = getter.get()
        assert geojson["type"] == "FeatureCollection"


def test_skip_download_and_simplify(tmp_path: Path, uk_lad_geojson_sample: str) -> None:
    """Assert that the file is not downloaded, it is loaded from disk, and then it is simplified and stored to disk with a new name."""
    with run_within_dir(tmp_path):
        getter = GeoJsonGetter("http://example.com/geojson", uk_lad_geojson_sample, 0.1)
        getter.get()
        assert Path(tmp_path, "lad-2023-sample.geojson").is_file()

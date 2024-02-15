from __future__ import annotations

from pathlib import Path

from map_uk.geojson.simplifier import GeoJsonSimplifier
from tests.utils import run_within_dir


def test_simplifier(tmp_path: Path, uk_lad_geojson_sample: str) -> None:
    """."""
    with run_within_dir(tmp_path):
        GeoJsonSimplifier(
            input_file_path=uk_lad_geojson_sample, output_file_path="simplified.geojson", tolerance=0.1
        ).simplify()
        assert Path(tmp_path, "simplified.geojson").is_file()
        size_file_original = Path(uk_lad_geojson_sample).stat().st_size
        size_file_simplified = Path("simplified.geojson").stat().st_size
        assert size_file_simplified < size_file_original

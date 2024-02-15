from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from map_uk.constants import Paths

@pytest.fixture()
def uk_lad_geojson_sample(tmp_path: Path) -> Path:
    """."""
    source_file = Paths.TEST_DIR / "data" / "lad-2023-sample.geojson"
    dest_dir = tmp_path / ".map_uk"
    dest_dir.mkdir(parents=True)
    shutil.copy(source_file, dest_dir)
    return Path(dest_dir) / "lad-2023-sample.geojson"

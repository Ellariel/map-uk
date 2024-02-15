from __future__ import annotations

from pathlib import Path

TOP_FOLDER = Path(__file__).resolve().parent.parent


class Paths:
    """Project paths."""

    TOP_FOLDER = TOP_FOLDER
    DATA_DIR: Path = TOP_FOLDER / "data"
    DOCS_DIR: Path = TOP_FOLDER / "docs"
    STATIC_DIR: Path = DOCS_DIR / "static"
    TEST_DIR: Path = TOP_FOLDER / "tests"

    @classmethod
    def ensure_directories_exist(cls) -> None:
        """Create directories if they don't exist."""
        directories = [
            getattr(cls, attr)
            for attr in dir(cls)
            if isinstance(getattr(cls, attr), Path)
        ]

        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)

Paths.ensure_directories_exist()

DEFAULT_MAP_ARGS = {"location": [53.774689, -1.735840], "zoom_start": 5, "tiles": "cartodb positron"}

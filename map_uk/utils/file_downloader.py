from __future__ import annotations

import logging
from pathlib import Path

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)


class FileDownloader:
    """A utility class for downloading files from a given URL."""

    def __init__(
        self,
        url: str,
        file_path: str | Path,
    ) -> None:
        """Args.

        url (str): The URL from where the file will be downloaded.
        file_path (str | Path): The local path where the downloaded file will be saved.

        """
        self.url = url
        self.file_path = Path(file_path)

    def download(self) -> None:
        """."""
        try:
            response = requests.get(self.url, stream=True, timeout=5)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            with Path.open(self.file_path, "wb") as file, tqdm(
                desc=self.file_path.name,
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            logger.info("Download successful.")

        except requests.HTTPError as e:
            logger.exception(
                "Failed to download %s. Status code: %s.",
                self.url,
                e.response.status_code,
            )

            msg = f"Error downloading {self.url}: {e}"
            raise Exception(msg) from None  # noqa: TRY002

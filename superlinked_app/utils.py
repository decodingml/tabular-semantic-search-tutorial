import gzip
from pathlib import Path

import requests
import zstandard
from loguru import logger


def download_file(url: str, output_path: Path) -> bool:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Get the file size from headers (if available)
        file_size = int(response.headers.get("content-length", 0))

        with output_path.open("wb") as file:
            if file_size == 0:
                file.write(response.content)
            else:
                downloaded = 0
                from tqdm import tqdm

                for chunk in tqdm(
                    response.iter_content(chunk_size=8192),
                    total=file_size // 8192,
                    unit="KB",
                    desc="Downloading",
                ):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
        return True

    except requests.exceptions.RequestException:
        logger.error("Failed to donwload the file.")

        return False


def decompress_zst(input_path: Path, output_path: Path) -> None:
    with open(input_path, "rb") as compressed:
        dctx = zstandard.ZstdDecompressor()
        with open(output_path, "wb") as destination:
            dctx.copy_stream(compressed, destination)


def decompress_gz(input_path: Path, output_path: Path) -> None:
    with gzip.open(input_path, "rb") as gz_file:
        with open(output_path, "wb") as output_file:
            output_file.write(gz_file.read())

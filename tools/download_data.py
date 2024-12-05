import gzip
from pathlib import Path

import zstandard


def decompress_zst(input_path: Path, output_path: Path):
    with open(input_path, "rb") as compressed:
        dctx = zstandard.ZstdDecompressor()
        with open(output_path, "wb") as destination:
            dctx.copy_stream(compressed, destination)


def decompress_gz(input_path: Path, output_path: Path):
    with gzip.open(input_path, "rb") as gz_file:
        with open(output_path, "wb") as output_file:
            output_file.write(gz_file.read())


# input_file = Path("data") / "esci.json.zst"
# output_file = Path("data") / "esci.json"

# decompress_zst(input_file, output_file)


input_file = Path("data") / "sample.json.gz"
output_file = Path("data") / "sample.json"
decompress_gz(input_file, output_file)

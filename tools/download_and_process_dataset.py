import argparse
from pathlib import Path

import pandas as pd
from loguru import logger

from superlinked_app import utils
from superlinked_app.data_processing import process_amazon_dataset

parser = argparse.ArgumentParser(description="Download and decompress data file")
parser.add_argument(
    "--data-url",
    help="URL of the file to download",
    default="https://github.com/shuttie/esci-s/raw/master/sample.json.gz",
)
parser.add_argument(
    "--data-dir",
    type=Path,
    help="Directory to save downloaded data",
    default=Path("data"),
)


def download_dataset(url: str, output_path: Path) -> Path:
    is_sample = url.endswith(".gz")

    # Set compressed file path based on compression type
    if is_sample:
        compressed_file_output_path = output_path / "sample.json.gz"
    else:
        compressed_file_output_path = output_path / "esci.json.zst"

    # Download file if it doesn't exist
    if not compressed_file_output_path.exists():
        logger.info(
            f"Downloading data from '{url}' to '{compressed_file_output_path}'."
        )
        successful = utils.download_file(url, compressed_file_output_path)
        if not successful:
            raise RuntimeError("Failed to download the requested file.")

    # Decompress file
    output_file = compressed_file_output_path.with_suffix("")
    logger.info(f"Decompressing '{compressed_file_output_path}' to '{output_file}'.")
    if is_sample:
        utils.decompress_gz(compressed_file_output_path, output_file)
    else:
        utils.decompress_zst(compressed_file_output_path, output_file)

    return output_file


if __name__ == "__main__":
    args = parser.parse_args()

    dataset_path = download_dataset(args.data_url, args.data_dir)

    logger.info("Processing dataset.")
    df = pd.read_json(str(dataset_path), lines=True)
    processed_df = process_amazon_dataset(df)

    for sample in [100, 300, len(df)]:
        sample = min(len(processed_df), sample)
        sampled_df_processed = processed_df.head(sample)

        processed_dataset_path = (
            dataset_path.parent
            / f"processed_{sample}_{dataset_path.name.replace('.json', '.jsonl')}"
        )
        logger.info(f"Saving processed dataset to '{processed_dataset_path}'.")
        sampled_df_processed.to_json(
            processed_dataset_path, orient="records", lines=True
        )

from pathlib import Path
from typing import Union
import polars as pl
import logging
from polars.exceptions import PolarsError
from src.utils.log_config import setup_logging

# Custom emojis
CUSTOM_EMOJIS = {
    "starting": "⏳",  # For "Starting data processing..."
    "loading": "📥",  # For "Loading data..."
    "completed": "✅",  # For "Processing completed"
    "success": "🎉",  # For "All files converted!"
    "warning": "⚠️",  # For warning messages
    "error": "❌",  # For error messages
    "saving": "💾",  # For "Saving results..."
    "config": "⚙️",  # For configuration messages
}


# Initialize the logger for this specific module.
setup_logging(console_level=logging.INFO, emoji_map=CUSTOM_EMOJIS)

logger = logging.getLogger(__name__)


def convert_data(path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """
    Convert a CSV file to Parquet format using Polars in a lazy manner.

    Args:
        path (Union[str, Path]): Path to the input CSV file.
        output_path (Union[str, Path]): Path where the Parquet file will be saved.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input file is not a CSV or if the output directory is invalid.
        PolarsError: If Polars fails to read the CSV or write the Parquet file.
    """
    input_path = Path(path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    if input_path.suffix.lower() != ".csv":
        raise ValueError(f"Input file must be a CSV, got: {input_path.suffix}")

    output_dir = output_path.parent
    if not output_dir.exists():
        raise ValueError(f"Output directory does not exist: {output_dir}")
    if output_path.suffix.lower() != ".parquet":
        raise ValueError(
            f"Output file must have .parquet extension, got: {output_path.suffix}"
        )

    try:
        logger.info(f"Starting data convertion of {input_path.name} to parquet")
        pl.scan_csv(input_path).sink_parquet(output_path)
        logger.info(f"The file {input_path.name} was successfully converted to parquet")
    except PolarsError as e:
        raise PolarsError(f"Failed to convert CSV to Parquet: {e}")

from pathlib import Path
import pytest
import polars as pl
import tempfile
import shutil
from src.data_understanding import data_collection


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_csv(temp_dir):
    """Create a sample CSV mimicking Porto Seguro's structure."""
    csv_path = temp_dir / "sample.csv"
    # Subset of Porto Seguro columns: numerical, categorical, binary, with -1 for missing
    df = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "target": [0, 1, 0],
            "ps_ind_01": [2, 5, -1],  # Numerical, -1 for missing
            "ps_ind_02_cat": [1, -1, 3],  # Categorical, -1 for missing
            "ps_car_13": [0.7, 0.9, 1.2],  # Numerical
        }
    )
    df.write_csv(csv_path)
    return csv_path


def test_convert_data_success(sample_csv, temp_dir):
    """Test successful conversion of a Porto Seguro-like CSV to Parquet."""
    output_path = temp_dir / "output.parquet"
    data_collection.convert_data(sample_csv, output_path)
    assert output_path.exists()
    assert output_path.is_file()
    # Verify the Parquet file preserves Porto Seguro structure
    df = pl.read_parquet(output_path)
    assert len(df) == 3
    assert df.columns == ["id", "target", "ps_ind_01", "ps_ind_02_cat", "ps_car_13"]
    assert df["ps_ind_01"].to_list() == [2, 5, -1]  # Check missing value handling
    assert df["target"].to_list() == [0, 1, 0]


def test_convert_data_nonexistent_input(temp_dir):
    """Test error when input file does not exist."""
    nonexistent_path = temp_dir / "nonexistent.csv"
    output_path = temp_dir / "output.parquet"
    with pytest.raises(FileNotFoundError, match="Input file does not exist"):
        data_collection.convert_data(nonexistent_path, output_path)


def test_convert_data_invalid_input_extension(temp_dir):
    """Test error when input file is not a CSV."""
    invalid_file = temp_dir / "data.txt"
    invalid_file.write_text("some text")
    output_path = temp_dir / "output.parquet"
    with pytest.raises(ValueError, match="Input file must be a CSV"):
        data_collection.convert_data(invalid_file, output_path)


def test_convert_data_not_a_file(temp_dir):
    """Test error when input path is a directory."""
    output_path = temp_dir / "output.parquet"
    with pytest.raises(ValueError, match="Input path is not a file"):
        data_collection.convert_data(temp_dir, output_path)


def test_convert_data_invalid_output_extension(temp_dir, sample_csv):
    """Test error when output file does not have .parquet extension."""
    invalid_output = temp_dir / "output.txt"
    with pytest.raises(ValueError, match="Output file must have .parquet extension"):
        data_collection.convert_data(sample_csv, invalid_output)


def test_convert_data_nonexistent_output_dir(sample_csv):
    """Test error when output directory does not exist."""
    invalid_output = Path("/nonexistent/directory/output.parquet")
    with pytest.raises(ValueError, match="Output directory does not exist"):
        data_collection.convert_data(sample_csv, invalid_output)


def test_convert_data_string_paths(sample_csv, temp_dir):
    """Test function works with string paths."""
    output_path = str(temp_dir / "output.parquet")
    data_collection.convert_data(str(sample_csv), output_path)
    assert Path(output_path).exists()


def test_convert_data_large_porto_seguro_like(temp_dir):
    """Test conversion of a larger Porto Seguro-like CSV to verify lazy evaluation."""
    csv_path = temp_dir / "large_sample.csv"
    # Simulate larger dataset (e.g., 10,000 rows)
    n_rows = 10000
    df = pl.DataFrame(
        {
            "id": range(n_rows),
            "target": [0] * (n_rows // 2) + [1] * (n_rows // 2),
            "ps_ind_01": [
                2 if i % 2 == 0 else -1 for i in range(n_rows)
            ],  # Missing values
            "ps_ind_02_cat": [1 if i % 3 == 0 else -1 for i in range(n_rows)],
            "ps_car_13": [0.7 + (i % 100) / 100 for i in range(n_rows)],
        }
    )
    df.write_csv(csv_path)
    output_path = temp_dir / "output.parquet"
    data_collection.convert_data(csv_path, output_path)
    assert output_path.exists()
    df_out = pl.read_parquet(output_path)
    assert len(df_out) == n_rows
    assert df_out.columns == ["id", "target", "ps_ind_01", "ps_ind_02_cat", "ps_car_13"]

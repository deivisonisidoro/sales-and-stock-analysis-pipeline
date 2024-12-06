from pathlib import Path

import pandas as pd
import pytest

from src.driver.dataloader import DataLoader

MOCK_CSV_DATA = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})


@pytest.fixture
def data_loader(mocker):
    """Fixture to create a DataLoader instance with mocked directory existence."""
    mocker.patch("pathlib.Path.exists", return_value=True)
    return DataLoader(base_path="mock_data")


def test_data_loader_init_directory_not_found(mocker):
    """Test that DataLoader raises FileNotFoundError if the base path does not exist."""
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="Diretório não encontrado: mock_data"):
        DataLoader(base_path="mock_data")

    mock_exists.assert_called_once()


def test_data_loader_load_csv_file_exists(mocker, data_loader):
    """Test that load_csv successfully loads a file when it exists."""
    mock_read_csv = mocker.patch("pandas.read_csv", return_value=MOCK_CSV_DATA)

    mock_exists_file = mocker.patch.object(Path, "exists", return_value=True)

    df = data_loader.load_csv("mock_file.csv")

    mock_exists_file.assert_called_once()
    mock_read_csv.assert_called_once_with(data_loader.base_path / "mock_file.csv")
    assert isinstance(df, pd.DataFrame)
    assert df.equals(MOCK_CSV_DATA)


def test_data_loader_load_csv_file_not_found(mocker, data_loader):
    """Test that load_csv raises FileNotFoundError when the file does not exist."""
    mock_exists_file = mocker.patch.object(Path, "exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="Arquivo não encontrado: mock_data/mock_file.csv"):
        data_loader.load_csv("mock_file.csv")

    mock_exists_file.assert_called_once()


def test_data_loader_extract_all(mocker, data_loader):
    """Test that extract_all loads multiple predefined CSV files."""
    mock_read_csv = mocker.patch("pandas.read_csv", return_value=MOCK_CSV_DATA)

    mock_exists_file = mocker.patch.object(Path, "exists", return_value=True)

    data = data_loader.extract_all()

    assert len(data) == 4
    for key in ["stock", "products", "store", "sales"]:
        assert key in data
        assert isinstance(data[key], pd.DataFrame)
        assert data[key].equals(MOCK_CSV_DATA)

    assert mock_read_csv.call_count == 4
    mock_exists_file.assert_called()

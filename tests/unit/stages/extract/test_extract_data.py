from tarfile import ExtractError
from unittest.mock import MagicMock

import pytest

from src.driver.interface.dataloader_interface import DataLoaderInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.stages.extract.extract_data import ExtractData


@pytest.fixture
def mock_dataloader() -> MagicMock:
    """Fixture para um DataLoader simulado."""
    mock = MagicMock(spec=DataLoaderInterface)
    return mock


def test_extract_data_success(mock_dataloader: MagicMock) -> None:
    """Teste para verificar a extração bem-sucedida dos dados."""

    mock_data = {
        "stock": "mock_stock_data",
        "store": "mock_store_data",
        "products": "mock_products_data",
        "sales": "mock_sales_data",
    }

    mock_dataloader.extract_all.return_value = mock_data

    extract_data_service = ExtractData(dataloader=mock_dataloader)

    result = extract_data_service.extract()

    assert isinstance(result, ExtractContract)

    assert result.data == mock_data


def test_extract_data_error(mock_dataloader: MagicMock) -> None:
    """Teste para verificar se a exceção ExtractError é levantada em caso de falha."""

    mock_dataloader.extract_all.side_effect = Exception("Erro durante a extração de dados")

    extract_data_service = ExtractData(dataloader=mock_dataloader)

    with pytest.raises(ExtractError, match="Erro durante a extração de dados"):
        extract_data_service.extract()


def test_extract_data_empty(mock_dataloader: MagicMock) -> None:
    """Teste para verificar o comportamento quando o DataLoader retorna dados vazios."""

    mock_dataloader.extract_all.return_value = {}

    extract_data_service = ExtractData(dataloader=mock_dataloader)

    result = extract_data_service.extract()

    assert result.data == {}

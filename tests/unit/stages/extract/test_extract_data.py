from tarfile import ExtractError

import pytest

from src.driver.interface.dataloader_interface import DataLoaderInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.stages.extract.extract_data import ExtractData


@pytest.fixture
def mock_dataloader(mocker):
    """
    Fixture para criar um mock de DataLoaderInterface.
    """
    return mocker.MagicMock(spec=DataLoaderInterface)


def test_extract_success(mock_dataloader):
    """
    Testa o comportamento do método extract em caso de sucesso.
    """

    mock_data = {
        "sales": [{"id": 1, "value": 100}],
        "stock": [{"id": 1, "quantity": 50}],
        "store": {"id": 1, "name": "Loja Teste"},
        "products": [{"id": 1, "name": "Produto Teste"}],
    }
    mock_dataloader.extract_all.return_value = mock_data

    service = ExtractData(mock_dataloader)

    result = service.extract()

    assert isinstance(result, ExtractContract)
    assert result.sales == mock_data["sales"]
    assert result.stock == mock_data["stock"]
    assert result.store == mock_data["store"]
    assert result.products == mock_data["products"]

    mock_dataloader.extract_all.assert_called_once()


def test_extract_failure(mock_dataloader):
    """
    Testa o comportamento do método extract quando ocorre uma exceção.
    """

    mock_dataloader.extract_all.side_effect = Exception("Erro ao extrair dados")

    service = ExtractData(mock_dataloader)

    with pytest.raises(ExtractError) as exc_info:
        service.extract()

    assert "Erro ao extrair dados" in str(exc_info.value)

    mock_dataloader.extract_all.assert_called_once()

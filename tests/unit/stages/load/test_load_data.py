from http.cookiejar import LoadError
from unittest.mock import MagicMock

import pandas as pd
import pytest
from pandas import DataFrame

from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.load.load_data import LoadData


@pytest.fixture
def mock_repository():
    """Mocka o repositório de banco de dados."""
    return MagicMock(spec=DatabaseRepositoryInterface)


def test_load_data_success(mock_repository):
    """Testa o método load quando tudo ocorre corretamente."""

    data = {
        "estoque_disponivel": pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "ESTOQUE_DISPONIVEL": [100, 200],
            }
        ),
        "velocidade_venda": pd.DataFrame(
            {
                "DATA_VENDA": ["2024-12-01", "2024-12-02"],
                "ID_FILIAL": [1, 2],
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "TAMANHO": ["P", "M"],
                "VENDA_PECAS": [10, 20],
                "VENDA_LIQUIDA": [1000, 2000],
                "VENDA_BRUTA": [1200, 2400],
                "ESTOQUE_DISPONIVEL": [50, 100],
                "VELOCIDADE_VENDA": [2.5, 3.0],
            }
        ),
    }

    load_data = LoadData(repository=mock_repository)

    load_data.load(data)

    mock_repository.create_table.assert_called()

    mock_repository.insert_data.assert_any_call(dataframe=data["estoque_disponivel"], table_name="estoque_disponivel")

    pd.testing.assert_frame_equal(data["velocidade_venda"], mock_repository.insert_data.call_args[1]["dataframe"])


def test_load_data_failure(mock_repository):
    """Testa o método load quando ocorre uma exceção ao inserir dados."""

    mock_repository.insert_data.side_effect = Exception("Erro ao inserir dados")

    data = {
        "estoque_disponivel": DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "ESTOQUE_DISPONIVEL": [100, 200],
            }
        )
    }

    load_data = LoadData(repository=mock_repository)

    with pytest.raises(LoadError, match="Erro ao inserir dados"):
        load_data.load(data)

    mock_repository.create_table.assert_called()
    mock_repository.insert_data.assert_called_once()

import pandas as pd
import pytest
import pytest_mock

from src.errors.load_error import LoadError
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.contracts.transform_contract import TransformContract
from src.stages.load.load_data import LoadData


@pytest.fixture
def mock_repository(mocker):
    """Mocka o repositório de banco de dados."""
    return mocker.MagicMock(spec=DatabaseRepositoryInterface)


def test_load_data_success(mock_repository, mocker: pytest_mock.MockerFixture):
    """Testa o método load quando tudo ocorre corretamente."""

    data = TransformContract(
        sales=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "VENDA_PECAS": [30, 50],
                "ID_FILIAL": [1, 2],
            }
        ),
        stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "TOTAL": [100, 200],
                "TRANSITO": [10, 20],
            }
        ),
        store=pd.DataFrame(
            {
                "ID_FILIAL": [1, 2],
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
            }
        ),
        products=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "DESCRICAO": ["Product A", "Product B"],
            }
        ),
        available_stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "ESTOQUE_DISPONIVEL": [100, 200],
            }
        ),
        sales_velocity=pd.DataFrame(
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
        sales_by_region=pd.DataFrame(
            {
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
                "VENDA_PECAS": [100, 200],
            }
        ),
    )

    load_data = LoadData(repository=mock_repository)

    # Executa o método
    load_data.load(data)

    # Verifica se o método create_table foi chamado
    mock_repository.create_table.assert_called()

    # Verifica se insert_data foi chamado com os argumentos corretos
    mock_repository.insert_data.assert_any_call(dataframe=mocker.ANY, table_name="available_stock")


def test_load_data_failure(mock_repository):
    """Testa o método load quando ocorre uma exceção ao inserir dados."""

    mock_repository.insert_data.side_effect = LoadError(message="Erro ao inserir dados")

    data = TransformContract(
        sales=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "VENDA_PECAS": [30, 50],
                "ID_FILIAL": [1, 2],
            }
        ),
        stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "TOTAL": [100, 200],
                "TRANSITO": [10, 20],
            }
        ),
        store=pd.DataFrame(
            {
                "ID_FILIAL": [1, 2],
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
            }
        ),
        products=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "DESCRICAO": ["Product A", "Product B"],
            }
        ),
        available_stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "ESTOQUE_DISPONIVEL": [100, 200],
            }
        ),
        sales_velocity=pd.DataFrame(
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
        sales_by_region=pd.DataFrame(
            {
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
                "VENDA_PECAS": [100, 200],
            }
        ),
    )

    load_data = LoadData(repository=mock_repository)

    with pytest.raises(LoadError, match="Erro ao inserir dados"):
        load_data.load(data)

    mock_repository.create_table.assert_called()
    mock_repository.insert_data.assert_called_once()


def test_load_data_table_creation_failure(mock_repository):
    """Testa o método load quando ocorre uma falha ao criar a tabela."""

    mock_repository.create_table.side_effect = LoadError(message="Erro ao criar tabela")

    data = TransformContract(
        sales=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "VENDA_PECAS": [30, 50],
                "ID_FILIAL": [1, 2],
            }
        ),
        stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Red", "Blue"],
                "TOTAL": [100, 200],
                "TRANSITO": [10, 20],
            }
        ),
        store=pd.DataFrame(
            {
                "ID_FILIAL": [1, 2],
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
            }
        ),
        products=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "DESCRICAO": ["Product A", "Product B"],
            }
        ),
        available_stock=pd.DataFrame(
            {
                "PRODUTO": ["A", "B"],
                "COR_PRODUTO": ["Azul", "Vermelho"],
                "ESTOQUE_DISPONIVEL": [100, 200],
            }
        ),
        sales_velocity=pd.DataFrame(
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
        sales_by_region=pd.DataFrame(
            {
                "UF": ["SP", "RJ"],
                "CIDADE": ["São Paulo", "Rio de Janeiro"],
                "VENDA_PECAS": [100, 200],
            }
        ),
    )

    load_data = LoadData(repository=mock_repository)

    with pytest.raises(LoadError, match="Erro ao criar tabela"):
        load_data.load(data)

    mock_repository.create_table.assert_called_once()


def test_load_data_invalid_data(mock_repository):
    """Testa o método load quando os dados fornecidos são inválidos."""

    # Dados inválidos (DataFrame vazio ou mal formado)
    data = TransformContract(
        sales=pd.DataFrame(),
        stock=pd.DataFrame(),
        store=pd.DataFrame(),
        products=pd.DataFrame(),
        available_stock=pd.DataFrame(),
        sales_velocity=pd.DataFrame(),
        sales_by_region=pd.DataFrame(),
    )

    load_data = LoadData(repository=mock_repository)

    with pytest.raises(ValueError):
        load_data.load(data)

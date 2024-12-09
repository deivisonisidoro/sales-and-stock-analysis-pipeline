from unittest import mock

import pytest

from src.analysis.interfaces.visualization_interface import VisualizerInterface
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.analysis.analyze_data import AnalyzeData
from src.stages.contracts.analyze_contract import AnalyzeContract


@pytest.fixture
def mock_visualizer():
    return mock.create_autospec(VisualizerInterface)


@pytest.fixture
def mock_repository():
    return mock.create_autospec(DatabaseRepositoryInterface)


@pytest.fixture
def analyze_data(mock_visualizer, mock_repository):
    return AnalyzeData(visualizer=mock_visualizer, repository=mock_repository)


def test_execute_analysis(analyze_data, mock_visualizer, mock_repository, mocker):
    # Mockando a leitura dos arquivos SQL
    mocker.patch.object(
        analyze_data,
        "_AnalyzeData__read_query_from_file",
        side_effect=["SELECT * FROM sales_velocity", "SELECT * FROM sales_by_region", "SELECT * FROM sales"],
    )

    # Mockando os resultados das consultas do repositório
    mock_repository.find.side_effect = [
        {"velocity": 100, "product": "A"},  # Resultado de sales_velocity
        {"region": "North", "sales": 500},  # Resultado de sales_by_region
        {"sales_id": 1, "amount": 1000},  # Resultado de sales
    ]

    # Chama o método que queremos testar
    analyze_data.execute_analysis()

    # Verificando se os métodos 'find' foram chamados corretamente
    mock_repository.find.assert_any_call(query="SELECT * FROM sales_velocity")
    mock_repository.find.assert_any_call(query="SELECT * FROM sales_by_region")
    mock_repository.find.assert_any_call(query="SELECT * FROM sales")

    # Verificando se o método 'analyze' foi chamado com o contrato correto
    analyze_contract = AnalyzeContract(
        sales_velocity={"velocity": 100, "product": "A"},
        sales_by_region={"region": "North", "sales": 500},
        sales={"sales_id": 1, "amount": 1000},
    )
    mock_visualizer.analyze.assert_called_once_with(analyze_contract)


def test_execute_analysis_when_queries_are_not_found(analyze_data, mock_visualizer, mock_repository, mocker):
    # Simulando a pasta de queries não encontrada
    mocker.patch.object(analyze_data, "_AnalyzeData__read_query_from_file", return_value=None)

    # Testa a execução sem resultados (nenhuma consulta é lida)
    analyze_data.execute_analysis()

    # Verificando que o método 'analyze' não foi chamado, pois não houve dados para analisar
    mock_visualizer.analyze.assert_not_called()

    # Verificando que o repositório não foi chamado
    mock_repository.find.assert_not_called()


def test_read_query_from_file_not_found(analyze_data, mocker):
    # Mocka a função __read_query_from_file para simular um arquivo não encontrado
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    # Verifica se o método lida corretamente com um erro ao tentar abrir o arquivo
    with pytest.raises(FileNotFoundError):
        analyze_data._AnalyzeData__read_query_from_file("non_existent_query.sql")

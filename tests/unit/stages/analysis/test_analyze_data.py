from unittest import mock

import pytest

from src.driver.visualization.interfaces.visualization_interface import ReportsVisualizerInterface
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.analysis.analyze_data import AnalyzeData


@pytest.fixture
def mock_visualizer():
    return mock.create_autospec(ReportsVisualizerInterface)


@pytest.fixture
def mock_repository():
    return mock.create_autospec(DatabaseRepositoryInterface)


@pytest.fixture
def analyze_data(mock_visualizer, mock_repository):
    return AnalyzeData(visualizer=mock_visualizer, repository=mock_repository)


@pytest.fixture
def mock_query_files(mocker):
    # Mocka a função `open` para simular leitura de arquivos de queries
    def mock_open(file_path, *args, **kwargs):
        query_mapping = {
            "queries/sales_velocity.sql": """
                SELECT produto, cor_produto, AVG(velocidade_venda) AS avg_velocidade_venda
                FROM sales_velocity
                GROUP BY produto, cor_produto
                ORDER BY avg_velocidade_venda DESC
                LIMIT 10;
            """,
            "queries/sales_by_branch.sql": """
                SELECT id_filial, SUM(venda_pecas) AS venda_pecas
                FROM sales
                GROUP BY id_filial;
            """,
            "queries/sales_by_product.sql": """
               SELECT produto, SUM(venda_pecas) AS venda_pecas
                FROM sales
                GROUP BY produto;
            """,
            "queries/top_10_least_sales_by_region.sql": """
                SELECT *
                FROM sales_by_region
                ORDER BY venda_pecas ASC;
            """,
            "queries/top_10_sales_by_region.sql": """
                SELECT *
                FROM sales_by_region
                ORDER BY venda_pecas DESC;
            """,
        }
        query_content = query_mapping.get(file_path)
        if query_content is None:
            raise FileNotFoundError(f"Query file not found: {file_path}")
        return mock.mock_open(read_data=query_content).return_value

    mocker.patch("builtins.open", mock_open)


def test_execute_analysis(analyze_data, mock_visualizer, mock_repository, mocker):
    # Configurar os resultados esperados das consultas no repositório
    mock_repository.find.side_effect = [
        [{"produto": "A", "cor_produto": "Vermelho", "avg_velocidade_venda": 100}],  # Resultado de sales_velocity
        [{"id_filial": 1, "venda_pecas": 200}],  # Resultado de sales_by_branch
        [{"produto": "A", "venda_pecas": 300}],  # Resultado de sales_by_product
        [{"region": "North", "venda_pecas": 50}],  # Resultado de top_10_least_sales_by_region
        [{"region": "South", "venda_pecas": 500}],  # Resultado de top_10_sales_by_region
    ]

    # Mockar o método __read_query_from_file para retornar os caminhos corretos das queries
    mocker.patch.object(
        analyze_data,
        "_AnalyzeData__read_query_from_file",
        side_effect=[
            """
                SELECT produto, cor_produto, AVG(velocidade_venda) AS avg_velocidade_venda
                FROM sales_velocity
                GROUP BY produto, cor_produto
                ORDER BY avg_velocidade_venda DESC
                LIMIT 10;
            """,
            "SELECT id_filial, SUM(venda_pecas) AS venda_pecas FROM sales GROUP BY id_filial;",
            "SELECT produto, SUM(venda_pecas) AS venda_pecas FROM sales GROUP BY produto;",
            "SELECT * FROM sales_by_region ORDER BY venda_pecas ASC;",
            "SELECT * FROM sales_by_region ORDER BY venda_pecas DESC;",
        ],
    )

    # Executar o método que está sendo testado
    analyze_data.execute_analysis()

    # Verificar se os métodos corretos foram chamados no visualizador
    mock_visualizer.generate_reports.assert_called_once()


def test_execute_analysis_when_queries_are_not_found(analyze_data, mock_visualizer, mock_repository, mocker):
    # Simulando a pasta de queries não encontrada
    mocker.patch.object(analyze_data, "_AnalyzeData__read_query_from_file", return_value=None)

    # Testa a execução sem resultados (nenhuma consulta é lida)
    analyze_data.execute_analysis()

    # Verificando que o método 'generate_reports' não foi chamado, pois não houve dados para analisar
    mock_visualizer.generate_reports.assert_not_called()

    # Verificando que o repositório não foi chamado
    mock_repository.find.assert_not_called()


def test_read_query_from_file_not_found(analyze_data, mocker):
    # Mocka a função __read_query_from_file para simular um arquivo não encontrado
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    # Verifica se o método lida corretamente com um erro ao tentar abrir o arquivo
    with pytest.raises(FileNotFoundError):
        analyze_data._AnalyzeData__read_query_from_file("non_existent_query.sql")

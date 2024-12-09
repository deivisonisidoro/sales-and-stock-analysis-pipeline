import os
import shutil

import pytest
import pytest_mock
from pandas import DataFrame

from src.analysis.visualization import SalesVisualizer


@pytest.fixture
def mock_sales_data() -> DataFrame:
    """Fixture que retorna um DataFrame com dados simulados de vendas."""
    return DataFrame(
        {
            "cidade": ["Cidade1", "Cidade2", "Cidade3"],
            "venda_pecas": [100, 200, 150],
        }
    )


@pytest.fixture
def visualizer() -> SalesVisualizer:
    """Fixture que instancia o SalesVisualizer com um diretório temporário."""
    return SalesVisualizer(output_directory="test_graphs")


def test_create_directory(visualizer: SalesVisualizer, mock_sales_data: DataFrame) -> None:
    """Teste para verificar se o diretório de saída foi criado."""
    visualizer.plot_sales_by_region(mock_sales_data)
    assert os.path.exists("test_graphs")

    for file in os.listdir("test_graphs"):
        file_path = os.path.join("test_graphs", file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)

    os.rmdir("test_graphs")


def test_plot_sales_by_region(
    visualizer: SalesVisualizer,
    mock_sales_data: DataFrame,
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Teste para a função plot_sales_by_region, verificando se os gráficos são gerados e salvos."""
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")
    visualizer.plot_sales_by_region(mock_sales_data)
    assert mock_savefig.call_count == 2
    mock_savefig.assert_any_call(os.path.join("test_graphs", "top_10_regioes_com_mais_vendas.png"))
    mock_savefig.assert_any_call(os.path.join("test_graphs", "top_10_regioes_com_menos_vendas.png"))


def test_plot_sales_velocity(visualizer: SalesVisualizer, mocker: pytest_mock.MockerFixture) -> None:
    """Teste para a função plot_sales_velocity, verificando se o gráfico é gerado corretamente."""
    velocity_data = DataFrame(
        {
            "produto": ["Produto1", "Produto2", "Produto3"],
            "cor_produto": ["Cor1", "Cor2", "Cor3"],
            "velocidade_venda": [5.5, 8.2, 7.1],
        }
    )

    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")
    visualizer.plot_sales_velocity(velocity_data)
    mock_savefig.assert_called_once_with(os.path.join("test_graphs", "top_10_produtos_maior_velocidade_venda.png"))


def test_plot_sales_by_group(visualizer: SalesVisualizer, mocker: pytest_mock.MockerFixture) -> None:
    """Teste para a função plot_sales_by_group, verificando se o gráfico de vendas por grupo é gerado."""
    sales_df = DataFrame(
        {
            "produto": ["Produto1", "Produto2", "Produto3"],
            "venda_pecas": [100, 200, 150],
            "id_filial": [1, 2, 3],
        }
    )

    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")
    visualizer.plot_sales_by_group(sales_df)
    mock_savefig.assert_any_call(os.path.join("test_graphs", "vendas_por_produto.png"))
    mock_savefig.assert_any_call(os.path.join("test_graphs", "vendas_por_filial.png"))

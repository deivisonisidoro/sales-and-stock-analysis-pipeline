import pandas as pd
import pytest

from src.driver.visualization.sales_by_group_visualizer import SalesByGroupVisualizer


@pytest.fixture
def vendas_df():
    """
    Fixture para fornecer um DataFrame de exemplo para os testes.
    """
    return pd.DataFrame(
        {
            "produto": ["Produto A", "Produto B", "Produto C"],
            "id_filial": ["Filial 1", "Filial 2", "Filial 1"],
            "venda_pecas": [100, 200, 150],
        }
    )


@pytest.fixture
def visualizer(tmp_path):
    """
    Fixture para instanciar o SalesByGroupVisualizer com um diretório temporário.
    """
    return SalesByGroupVisualizer(output_directory=str(tmp_path))


def test_plot_sales_by_product(visualizer, vendas_df, mocker):
    """
    Testa a geração do gráfico de vendas por produto.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_sales_by_product(vendas_df)

    # Verifica se o gráfico foi salvo no diretório correto
    mock_savefig.assert_called_once_with(mocker.ANY)


def test_plot_sales_by_branch(visualizer, vendas_df, mocker):
    """
    Testa a geração do gráfico de vendas por filial.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_sales_by_branch(vendas_df)

    # Verifica se o gráfico foi salvo no diretório correto
    mock_savefig.assert_called_once_with(mocker.ANY)


def test_output_filenames(visualizer, vendas_df, mocker):
    """
    Verifica se os arquivos possuem os nomes esperados.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_sales_by_product(vendas_df)
    mock_savefig.assert_any_call(visualizer.output_directory + "/vendas_por_produto.png")

    visualizer.plot_sales_by_branch(vendas_df)
    mock_savefig.assert_any_call(visualizer.output_directory + "/vendas_por_filial.png")

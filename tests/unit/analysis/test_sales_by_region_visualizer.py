import pandas as pd
import pytest

from src.driver.visualization.sales_by_region_visualizer import SalesByRegionVisualizer


@pytest.fixture
def sales_by_region_df():
    """
    Fixture para fornecer um DataFrame de exemplo para os testes.
    """
    return pd.DataFrame(
        {
            "cidade": [
                "Cidade A",
                "Cidade B",
                "Cidade C",
                "Cidade D",
                "Cidade E",
                "Cidade F",
                "Cidade G",
                "Cidade H",
                "Cidade I",
                "Cidade J",
                "Cidade K",
            ],
            "venda_pecas": [500, 400, 350, 300, 250, 200, 150, 100, 90, 80, 70],
        }
    )


@pytest.fixture
def visualizer(tmp_path):
    """
    Fixture para instanciar o SalesByRegionVisualizer com um diretório temporário.
    """
    return SalesByRegionVisualizer(output_directory=str(tmp_path))


def test_plot_top_10_sales_by_region(visualizer, sales_by_region_df, mocker):
    """
    Testa a geração do gráfico das 10 regiões com mais vendas.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_top_10_sales_by_region(sales_by_region_df)

    # Verifica se o gráfico foi salvo no diretório correto
    mock_savefig.assert_called_once_with(f"{visualizer.output_directory}/top_10_regioes_com_mais_vendas.png")


def test_plot_top_10_least_sales_by_region(visualizer, sales_by_region_df, mocker):
    """
    Testa a geração do gráfico das 10 regiões com menos vendas.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_top_10_least_sales_by_region(sales_by_region_df)

    # Verifica se o gráfico foi salvo no diretório correto
    mock_savefig.assert_called_once_with(f"{visualizer.output_directory}/top_10_regioes_com_menos_vendas.png")


def test_output_filenames(visualizer, sales_by_region_df, mocker):
    """
    Verifica se os arquivos possuem os nomes esperados.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_top_10_sales_by_region(sales_by_region_df)
    mock_savefig.assert_any_call(f"{visualizer.output_directory}/top_10_regioes_com_mais_vendas.png")

    visualizer.plot_top_10_least_sales_by_region(sales_by_region_df)
    mock_savefig.assert_any_call(f"{visualizer.output_directory}/top_10_regioes_com_menos_vendas.png")

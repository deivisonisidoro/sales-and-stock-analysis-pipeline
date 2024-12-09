import pandas as pd
import pytest

from src.analysis.visualization.sales_velocity_visualizer import SalesVelocityVisualizer


@pytest.fixture
def sales_velocity_df():
    """
    Fixture para fornecer um DataFrame de exemplo para os testes.
    """
    return pd.DataFrame(
        {
            "produto": [
                "Produto A",
                "Produto B",
                "Produto C",
                "Produto D",
                "Produto E",
                "Produto F",
                "Produto G",
                "Produto H",
                "Produto I",
                "Produto J",
                "Produto K",
            ],
            "avg_velocidade_venda": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5],
        }
    )


@pytest.fixture
def visualizer(tmp_path):
    """
    Fixture para instanciar o SalesVelocityVisualizer com um diretório temporário.
    """
    return SalesVelocityVisualizer(output_directory=str(tmp_path))


def test_plot_sales_velocity(visualizer, sales_velocity_df, mocker):
    """
    Testa a geração do gráfico de velocidade de vendas.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_sales_velocity(sales_velocity_df)

    # Verifica se o gráfico foi salvo no diretório correto
    mock_savefig.assert_called_once_with(f"{visualizer.output_directory}/top_10_produtos_maior_velocidade_venda.png")


def test_output_filename(visualizer, sales_velocity_df, mocker):
    """
    Verifica se o arquivo possui o nome esperado.
    """
    mock_savefig = mocker.patch("matplotlib.pyplot.savefig")

    visualizer.plot_sales_velocity(sales_velocity_df)

    # Verifica a chamada para salvar o gráfico
    mock_savefig.assert_called_with(f"{visualizer.output_directory}/top_10_produtos_maior_velocidade_venda.png")

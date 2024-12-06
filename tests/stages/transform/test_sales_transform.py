import pandas as pd

from src.stages.transform.sales_transform import SalesTransformer


def test_calculate_sales_velocity():
    """Testa o método calculate_sales_velocity da classe SalesTransformer."""

    sales_data = {
        "PRODUTO": ["A", "B", "C"],
        "COR_PRODUTO": ["Vermelho", "Azul", "Preto"],
        "VENDA_PECAS": [10, 15, 5],
    }
    sales_df = pd.DataFrame(sales_data)

    stock_data = {
        "PRODUTO": ["A", "B", "C"],
        "COR_PRODUTO": ["Vermelho", "Azul", "Preto"],
        "ESTOQUE_DISPONIVEL": [100, 50, 0],
    }
    stock_df = pd.DataFrame(stock_data)

    result_df = SalesTransformer.calculate_sales_velocity(sales_df, stock_df)

    expected_data = {
        "PRODUTO": ["A", "B"],
        "COR_PRODUTO": ["Vermelho", "Azul"],
        "VENDA_PECAS": [10, 15],
        "ESTOQUE_DISPONIVEL": [100, 50],
        "VELOCIDADE_VENDA": [0.1, 0.3],
    }
    expected_df = pd.DataFrame(expected_data)

    result_df["VELOCIDADE_VENDA"] = result_df["VELOCIDADE_VENDA"].astype("float64")
    expected_df["VELOCIDADE_VENDA"] = expected_df["VELOCIDADE_VENDA"].astype("float64")

    pd.testing.assert_frame_equal(result_df, expected_df)

import pandas as pd

from src.stages.transform.stock_transformer import StockTransformer


def test_calculate_available_stock():
    """Testa o método calculate_available_stock da classe StockTransformer."""

    stock_data = {
        "PRODUTO": ["A", "B", "A", "B", "C"],
        "COR_PRODUTO": ["Vermelho", "Azul", "Vermelho", "Azul", "Preto"],
        "TOTAL": [100, 150, 200, 300, 50],
        "TRANSITO": [20, 30, 50, 60, 10],
    }
    stock_df = pd.DataFrame(stock_data)

    result_df = StockTransformer.calculate_available_stock(stock_df)

    expected_data = {
        "PRODUTO": ["A", "B", "C"],
        "COR_PRODUTO": ["Vermelho", "Azul", "Preto"],
        "ESTOQUE_DISPONIVEL": [230, 360, 40],
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = result_df.groupby(["PRODUTO", "COR_PRODUTO"], as_index=False).sum()

    pd.testing.assert_frame_equal(result_df, expected_df)

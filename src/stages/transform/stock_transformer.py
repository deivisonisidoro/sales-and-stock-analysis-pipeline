import pandas as pd


class StockTransformer:
    """Responsável pelas transformações relacionadas ao estoque."""

    @staticmethod
    def calculate_available_stock(stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula o estoque disponível subtraindo 'TRANSITO' de 'TOTAL',
        e agrega os dados por 'PRODUTO' e 'COR_PRODUTO'.

        Args:
            stock_df (pd.DataFrame): DataFrame contendo dados de estoque.

        Returns:
            pd.DataFrame: DataFrame transformado com o estoque disponível.
        """
        stock_df["ESTOQUE_DISPONIVEL"] = stock_df["TOTAL"] - stock_df["TRANSITO"]
        aggregated_df = stock_df.groupby(["PRODUTO", "COR_PRODUTO"]).agg({"ESTOQUE_DISPONIVEL": "sum"}).reset_index()

        return aggregated_df

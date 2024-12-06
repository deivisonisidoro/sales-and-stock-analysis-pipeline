import pandas as pd


class SalesTransformer:
    """Responsável pelas transformações relacionadas a vendas."""

    @staticmethod
    def calculate_sales_velocity(sales_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula a velocidade de vendas ao combinar dados de vendas e estoque.

        Args:
            sales_df (pd.DataFrame): DataFrame contendo dados de vendas.
            stock_df (pd.DataFrame): DataFrame contendo dados de estoque.

        Returns:
            pd.DataFrame: DataFrame transformado com a velocidade de vendas.
        """
        merged_df = pd.merge(sales_df, stock_df, on=["PRODUTO", "COR_PRODUTO"], how="inner")
        merged_df["VELOCIDADE_VENDA"] = merged_df["VENDA_PECAS"] / (merged_df["ESTOQUE_DISPONIVEL"].replace(0, None))
        merged_df = merged_df.dropna(subset=["VELOCIDADE_VENDA"])
        return merged_df

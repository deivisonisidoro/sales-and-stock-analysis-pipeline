from pandas import DataFrame


class SalesByRegionAnalyzer:
    """
    Classe responsável por analisar os dados de vendas por região.
    """

    @staticmethod
    def calculate_sales_by_region(sales_df: DataFrame, store_df: DataFrame) -> DataFrame:
        """
        Realiza a análise de vendas por região, agrupando os dados por estado (UF) e cidade.

        Args:
            sales_df (DataFrame): DataFrame contendo os dados de vendas.
            store_df (DataFrame): DataFrame contendo os dados das lojas.

        Returns:
            DataFrame: Dados agregados de vendas, agrupados por UF e cidade, com o total de peças vendidas.
        """
        sales_region = sales_df.merge(store_df, on="ID_FILIAL", how="inner")

        return sales_region.groupby(["UF", "CIDADE"]).agg({"VENDA_PECAS": "sum"}).reset_index()

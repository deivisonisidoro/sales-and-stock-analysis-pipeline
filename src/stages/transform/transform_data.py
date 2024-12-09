import pandas as pd

from src.stages.contracts.extract_contract import ExtractContract
from src.stages.contracts.transform_contract import TransformContract


class TransformData:
    """Classe responsável por coordenar as transformações dos dados."""

    def transform(self, extract_contract: "ExtractContract") -> "TransformContract":
        """
        Executa a transformação dos dados a partir do contrato de entrada.

        Args:
            extract_contract (ExtractContract): O contrato de dados a ser transformado.

        Returns:
            TransformContract: O contrato de dados transformados.
        """
        stock = self._clean_data(extract_contract.stock)
        sales = self._clean_data(extract_contract.sales)
        products = self._clean_data(extract_contract.products)
        store = self._clean_data(extract_contract.store)

        available_stock = self._calculate_available_stock(stock.copy())

        sales_velocity = self._calculate_sales_velocity(sales, available_stock)

        sales_by_region = self._calculate_sales_by_region(sales, store)

        transform_contract = TransformContract(
            sales_velocity=sales_velocity,
            available_stock=available_stock,
            sales_by_region=sales_by_region,
            store=store,
            sales=sales,
            stock=stock,
            products=products,
        )

        return transform_contract

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa os dados removendo duplicatas e preenchendo valores ausentes.

        Args:
            df (pd.DataFrame): O DataFrame a ser limpo.

        Returns:
            pd.DataFrame: DataFrame limpo.
        """
        cleaned_df = df.drop_duplicates().fillna(0)
        return cleaned_df

    def _calculate_sales_velocity(self, sales_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
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

    def _calculate_available_stock(self, stock_df: pd.DataFrame) -> pd.DataFrame:
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

    def _calculate_sales_by_region(self, sales_df: pd.DataFrame, store_df: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza a transformação de dados de vendas por região, agrupando por estado (UF) e cidade.

        Args:
            sales_df (DataFrame): DataFrame contendo os dados de vendas.
            store_df (DataFrame): DataFrame contendo os dados das lojas.
        Returns:
            DataFrame: Dados de vendas agregados por UF e cidade, com o total de peças vendidas.
        """
        sales_region = sales_df.merge(store_df, on="ID_FILIAL", how="inner")
        aggregated_sales = sales_region.groupby(["UF", "CIDADE"]).agg({"VENDA_PECAS": "sum"}).reset_index()
        return aggregated_sales

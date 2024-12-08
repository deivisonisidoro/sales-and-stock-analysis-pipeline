from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class ExtractContract:
    """Contrato de extração de dados.

    Contém os dados extraídos de vendas e de estoque a serem transformados.

    Attributes:
        sales_data (DataFrame): Dados de vendas extraídos.
        stock_data (DataFrame): Dados de estoque extraídos.
        products (DataFrame): Dados de produtos extraídos.
    """

    sales: DataFrame
    stock: DataFrame
    store: DataFrame
    products: DataFrame

from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class ExtractContract:
    """
    Contrato de extração de dados.

    Esta classe representa o contrato contendo os dados extraídos de vendas, estoque, lojas e produtos.
    Esses dados serão utilizados posteriormente nas etapas de transformação dentro do pipeline ETL.

    Attributes:
        sales (DataFrame): Dados extraídos relacionados às vendas.
        stock (DataFrame): Dados extraídos relacionados ao estoque.
        store (DataFrame): Dados extraídos relacionados às lojas.
        products (DataFrame): Dados extraídos relacionados aos produtos.
    """

    sales: DataFrame
    stock: DataFrame
    store: DataFrame
    products: DataFrame

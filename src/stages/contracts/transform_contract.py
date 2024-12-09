from dataclasses import dataclass

import pandas as pd


@dataclass
class TransformContract:
    """
    Contrato de dados transformados.

    Contém os dados que foram transformados e estão prontos para análise e carga.
    Esses dados incluem informações sobre a velocidade de vendas, estoque disponível,
    vendas por região, estoque, vendas, produtos e lojas.

    Attributes:
        sales_velocity (pd.DataFrame): Dados transformados que indicam a velocidade de vendas.
        available_stock (pd.DataFrame): Dados transformados sobre o estoque disponível.
        sales_by_region (pd.DataFrame): Dados transformados sobre as vendas agregadas por região.
        stock (pd.DataFrame): Dados transformados sobre o estoque.
        sales (pd.DataFrame): Dados transformados sobre as vendas realizadas.
        products (pd.DataFrame): Dados transformados sobre os produtos disponíveis.
        store (pd.DataFrame): Dados transformados sobre as lojas.
    """

    sales_velocity: pd.DataFrame
    available_stock: pd.DataFrame
    sales_by_region: pd.DataFrame
    stock: pd.DataFrame
    sales: pd.DataFrame
    products: pd.DataFrame
    store: pd.DataFrame

from dataclasses import dataclass

import pandas as pd


@dataclass
class TransformContract:
    """Contrato de dados transformados.

    Contém os dados transformados de velocidade de vendas, estoque disponível
    e vendas por região.

    Attributes:
        sales_velocity (pd.DataFrame): Dados de velocidade de vendas transformados.
        available_stock (pd.DataFrame): Dados de estoque disponível transformados.
        sales_by_region (pd.DataFrame): Dados de vendas agregados por região.
    """

    sales_velocity: pd.DataFrame
    available_stock: pd.DataFrame
    sales_by_region: pd.DataFrame
    stock: pd.DataFrame
    sales: pd.DataFrame
    products: pd.DataFrame
    store: pd.DataFrame

from dataclasses import dataclass

import pandas as pd


@dataclass
class AnalyzeContract:
    """
    Contrato de dados transformados.

    Esta classe contém os dados que foram transformados e estão prontos para serem carregados no banco de dados.
    Os dados incluem informações sobre a velocidade de vendas, estoque disponível e vendas por região.

    Attributes:
        sales_velocity (pd.DataFrame): Dados transformados que indicam a velocidade de vendas.
        sales_by_region (pd.DataFrame): Dados transformados sobre as vendas agregadas por região.
        sales (pd.DataFrame): Dados de vendas transformados, que contêm informações detalhadas sobre vendas realizadas.
    """

    sales_velocity: pd.DataFrame
    sales_by_product: pd.DataFrame
    sales_by_branch: pd.DataFrame
    top_10_sales_by_region: pd.DataFrame
    top_10_least_sales_by_region: pd.DataFrame

from abc import ABC, abstractmethod

from pandas import DataFrame

from src.infra.interface.database_repository import DatabaseRepositoryInterface


class VisualizerInterface(ABC):
    """
    Interface para a classe Visualizer.
    Define os contratos para a visualização de dados.
    """

    @abstractmethod
    def __init__(self, repository: DatabaseRepositoryInterface, output_directory: str = "graphs") -> None:
        """
        Inicializa o visualizador e configura o diretório de saída para salvar os gráficos.

        Args:
            repository (DatabaseRepositoryInterface): O repositório de dados utilizado para obter os dados de vendas.
            output_directory (str): O diretório onde os gráficos serão salvos.
        """
        pass

    @abstractmethod
    def analyze(self, sales_by_region: DataFrame) -> None:
        """
        Analisa os dados e gera os gráficos correspondentes.

        Args:
            analyze_contract (AnalyzeContract): Contrato contendo os dados.
        """
        pass

    @abstractmethod
    def plot_sales_by_region(self, sales_by_region: DataFrame) -> None:
        """
        Gera um gráfico de vendas por região.

        Args:
            sales_by_region (DataFrame): Dados de vendas agrupados por região.
        """
        pass

    @abstractmethod
    def plot_sales_velocity(self, sales_velocity: DataFrame) -> None:
        """
        Gera um gráfico de velocidade de vendas.

        Args:
            sales_velocity (DataFrame): Dados de velocidade de vendas.
        """
        pass

    @abstractmethod
    def plot_sales_by_group(self, vendas_df: DataFrame) -> None:
        """
        Gera gráficos de vendas por produto e filial.

        Args:
            vendas_df (DataFrame): Dados de vendas.
        """
        pass

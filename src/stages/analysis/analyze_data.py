import os

from src.analysis.interfaces.visualization_interface import VisualizerInterface
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.contracts.analyze_contract import AnalyzeContract


class AnalyzeData:
    def __init__(self, visualizer: VisualizerInterface, repository: DatabaseRepositoryInterface):
        """
        Inicializa a classe AnalyzeData.

        Args:
            visualizer (VisualizerInterface): A interface para a visualização dos dados analisados.
            repository (DatabaseRepositoryInterface): O repositório para buscar os dados necessários para análise.
        """
        self.__visualizer = visualizer
        self.__repository = repository

    def execute_analysis(self) -> None:
        """
        Executa a análise dos dados de vendas e aciona a visualização.

        Este método busca os dados de vendas a partir do repositório, cria um contrato de análise
        com os dados adquiridos e passa esse contrato para o visualizador responsável pela
        criação dos gráficos e visualizações.
        """
        sales_velocity_query = self.__read_query_from_file("sales_velocity.sql")
        sales_by_region_query = self.__read_query_from_file("sales_by_region.sql")
        sales_query = self.__read_query_from_file("sales.sql")

        if not all([sales_velocity_query, sales_by_region_query, sales_query]):
            print("Uma ou mais consultas não foram encontradas.")
            return

        sales_velocity = self.__repository.find(query=sales_velocity_query)
        sales_by_region = self.__repository.find(query=sales_by_region_query)
        sales = self.__repository.find(query=sales_query)

        analyze_contract = AnalyzeContract(sales_velocity=sales_velocity, sales_by_region=sales_by_region, sales=sales)

        self.__visualizer.analyze(analyze_contract)

    def __read_query_from_file(self, filename: str) -> str:
        """
        Lê o conteúdo de uma consulta SQL a partir de um arquivo.

        Args:
            filename (str): O nome do arquivo contendo a consulta SQL.

        Returns:
            str: O conteúdo da consulta SQL.
        """
        queries_dir = "src/queries/analysis"

        if not os.path.exists(queries_dir):
            print(f"A pasta {queries_dir} não foi encontrada!")
            return

        if filename.endswith(".sql"):
            file_path = os.path.join(queries_dir, filename)
            with open(file_path, "r") as file:
                return file.read()

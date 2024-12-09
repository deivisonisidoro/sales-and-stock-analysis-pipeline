import os

from src.stages.contracts.analyze_contract import AnalyzeContract

from .interfaces.visualization_interface import ReportsVisualizerInterface
from .sales_by_group_visualizer import SalesByGroupVisualizer
from .sales_by_region_visualizer import SalesByRegionVisualizer
from .sales_velocity_visualizer import SalesVelocityVisualizer


class ReportsVisualizer(ReportsVisualizerInterface):
    """
    Classe responsável por visualizar e salvar gráficos relacionados a dados de relatórios.
    """

    def __init__(self, output_directory: str = "graphs"):
        """
        Inicializa o visualizador e configura o diretório de saída para salvar os gráficos.

        Args:
            output_directory (str): O diretório onde os gráficos serão salvos. Padrão é "graphs".
        """
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

        self.sales_by_region_visualizer = SalesByRegionVisualizer(self.output_directory)
        self.sales_velocity_visualizer = SalesVelocityVisualizer(self.output_directory)
        self.sales_by_group_visualizer = SalesByGroupVisualizer(self.output_directory)

    def generate_reports(self, analyze_contract: AnalyzeContract) -> None:
        """
        Gera relatórios visuais (gráficos) relacionados aos dados fornecidos.

        Args:
            analyze_contract (AnalyzeContract): Contrato contendo os dados para gerar os relatórios.
        """
        self.sales_by_region_visualizer.plot_top_10_sales_by_region(analyze_contract.sales_by_region)
        self.sales_by_region_visualizer.plot_top_10_least_sales_by_region(analyze_contract.sales_by_region)
        self.sales_velocity_visualizer.plot_sales_velocity(analyze_contract.sales_velocity)
        self.sales_by_group_visualizer.plot_sales_by_product(analyze_contract.sales)
        self.sales_by_group_visualizer.plot_sales_by_branch(analyze_contract.sales)

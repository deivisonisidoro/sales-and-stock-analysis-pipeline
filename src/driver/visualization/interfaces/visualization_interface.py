from abc import ABC, abstractmethod

from src.stages.contracts.analyze_contract import AnalyzeContract


class ReportsVisualizerInterface(ABC):
    """
    Interface para a classe ReportsVisualizer.
    Define os contratos para a visualização de dados.
    """

    @abstractmethod
    def generate_reports(self, analyze_contract: AnalyzeContract) -> None:
        """
        Gera relatórios visuais (gráficos) relacionados aos dados fornecidos.

        Args:
            analyze_contract (AnalyzeContract): Contrato contendo os dados para gerar os relatórios.
        """
        pass

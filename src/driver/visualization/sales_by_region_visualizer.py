import os

import matplotlib.pyplot as plt
from pandas import DataFrame


class SalesByRegionVisualizer:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    def plot_top_10_sales_by_region(self, sales_by_region: DataFrame) -> None:
        """
        Visualiza e salva o gráfico de vendas por região, mostrando as 10 regiões com mais vendas.

        Args:
            sales_by_region (DataFrame): Dados agregados de vendas agrupados por região.
        """

        plt.figure(figsize=(10, 6))
        plt.bar(
            sales_by_region["cidade"][:10],
            sales_by_region["venda_pecas"][:10],
            color="skyblue",
        )
        plt.title("Top 10 Regiões com Mais Vendas")
        plt.xlabel("Cidade")
        plt.ylabel("Vendas (Peças)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_regioes_com_mais_vendas.png"))
        plt.close()

    def plot_top_10_least_sales_by_region(self, sales_by_region: DataFrame) -> None:
        """
        Visualiza e salva o gráfico de vendas por região, mostrando as 10 regiões com menos vendas.

        Args:
            sales_by_region (DataFrame): Dados agregados de vendas agrupados por região.
        """

        plt.figure(figsize=(10, 6))
        plt.bar(
            sales_by_region["cidade"][:10],
            sales_by_region["venda_pecas"][:10],
            color="salmon",
        )
        plt.title("Top 10 Regiões com Menos Vendas")
        plt.xlabel("Cidade")
        plt.ylabel("Vendas (Peças)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_regioes_com_menos_vendas.png"))
        plt.close()

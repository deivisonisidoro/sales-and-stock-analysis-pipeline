import os

import matplotlib.pyplot as plt
from pandas import DataFrame


class SalesVelocityVisualizer:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    def plot_sales_velocity(self, sales_velocity: DataFrame) -> None:
        """
        Visualiza e salva os 10 principais produtos por velocidade de venda.

        Args:
            sales_velocity (DataFrame): Dados de velocidade de vendas.
        """
        # Agrupar e ordenar por velocidade de vendas
        plt.figure(figsize=(10, 6))
        plt.bar(
            sales_velocity["produto"][:10],
            sales_velocity["avg_velocidade_venda"][:10],
            color="lightgreen",
        )
        plt.title("Top 10 Produtos com Maior Velocidade de Venda")
        plt.xlabel("Produto")
        plt.ylabel("Velocidade de Venda")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_produtos_maior_velocidade_venda.png"))
        plt.close()

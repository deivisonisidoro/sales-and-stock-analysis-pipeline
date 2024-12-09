import os

import matplotlib.pyplot as plt
from pandas import DataFrame


class SalesByGroupVisualizer:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    def plot_sales_by_product(self, vendas_df: DataFrame) -> None:
        """
        Visualiza e salva o gráfico de vendas por produto.

        Args:
            vendas_df (DataFrame): Dados de vendas.
        """
        vendas_por_produto = vendas_df.groupby(["produto"]).agg({"venda_pecas": "sum"}).reset_index()

        plt.figure(figsize=(12, 8))
        plt.bar(
            vendas_por_produto["produto"],
            vendas_por_produto["venda_pecas"],
            color="orange",
        )
        plt.title("Vendas por Produto")
        plt.xlabel("Produto")
        plt.ylabel("Vendas (Peças)")
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.tight_layout(pad=3.0)
        plt.savefig(os.path.join(self.output_directory, "vendas_por_produto.png"))
        plt.close()

    def plot_sales_by_branch(self, vendas_df: DataFrame) -> None:
        """
        Visualiza e salva o gráfico de vendas por filial.

        Args:
            vendas_df (DataFrame): Dados de vendas.
        """
        vendas_por_filial = vendas_df.groupby(["id_filial"]).agg({"venda_pecas": "sum"}).reset_index()

        plt.figure(figsize=(10, 6))
        plt.bar(
            vendas_por_filial["id_filial"],
            vendas_por_filial["venda_pecas"],
            color="purple",
        )
        plt.title("Vendas por Filial")
        plt.xlabel("Filial")
        plt.ylabel("Vendas (Peças)")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "vendas_por_filial.png"))
        plt.close()

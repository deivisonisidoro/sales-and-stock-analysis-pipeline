import os

import matplotlib.pyplot as plt
from pandas import DataFrame

from src.stages.contracts.load_contract import LoadContract


class SalesVisualizer:
    """
    Classe responsável por visualizar e salvar gráficos relacionados a dados de vendas.
    """

    def __init__(self, output_directory: str = "graphs"):
        """
        Inicializa o visualizador e configura o diretório de saída para salvar os gráficos.

        Args:
            output_directory (str): O diretório onde os gráficos serão salvos. Padrão é "graphs".
        """
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def analyze(self, load_contract: LoadContract) -> None:
        """
        Analisa os dados de vendas fornecidos e gera os gráficos correspondentes.

        Args:
            load_contract (LoadContract): Contrato contendo os dados de vendas.
        """
        self.__plot_sales_by_region(load_contract.sales_by_region)
        self.__plot_sales_velocity(load_contract.sales_velocity)
        self.__plot_sales_by_group(load_contract.sales)

    def __plot_sales_by_region(self, sales_by_region: DataFrame) -> None:
        """
        Visualiza e salva gráficos de vendas por região.

        Args:
            sales_by_region (DataFrame): Dados agregados de vendas agrupados por região.
        """
        # Ordenar regiões pelo total de vendas (decrescente)
        sales_by_region = sales_by_region.sort_values(by="venda_pecas", ascending=False)

        # Top 10 regiões com mais vendas
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

        # Top 10 regiões com menos vendas
        sales_by_region = sales_by_region.sort_values(by="venda_pecas", ascending=True)
        plt.figure(figsize=(10, 6))
        plt.bar(
            sales_by_region["cidade"][-10:],
            sales_by_region["venda_pecas"][-10:],
            color="salmon",
        )
        plt.title("Top 10 Regiões com Menos Vendas")
        plt.xlabel("Cidade")
        plt.ylabel("Vendas (Peças)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_regioes_com_menos_vendas.png"))
        plt.close()

    def __plot_sales_velocity(self, sales_velocity: DataFrame) -> None:
        """
        Visualiza e salva os 10 principais produtos por velocidade de venda.

        Args:
            sales_velocity (DataFrame): Dados de velocidade de vendas.
        """
        # Agrupar e ordenar por velocidade de vendas
        velocity_by_product = (
            sales_velocity.groupby(["produto", "cor_produto"]).agg({"velocidade_venda": "mean"}).reset_index()
        )
        velocity_by_product = velocity_by_product.sort_values(by="velocidade_venda", ascending=False)

        # Top 10 produtos por velocidade de vendas
        plt.figure(figsize=(10, 6))
        plt.bar(
            velocity_by_product["produto"][:10],
            velocity_by_product["velocidade_venda"][:10],
            color="lightgreen",
        )
        plt.title("Top 10 Produtos com Maior Velocidade de Venda")
        plt.xlabel("Produto")
        plt.ylabel("Velocidade de Venda")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_produtos_maior_velocidade_venda.png"))
        plt.close()

    def __plot_sales_by_group(self, vendas_df: DataFrame) -> None:
        """
        Visualiza e salva gráficos de vendas por produto e filial.

        Args:
            vendas_df (DataFrame): Dados de vendas.
        """
        # Vendas por produto
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

        # Vendas por filial
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

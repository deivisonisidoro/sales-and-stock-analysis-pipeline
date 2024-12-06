import os

import matplotlib.pyplot as plt
from pandas import DataFrame


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

    def plot_sales_by_region(self, vendas_regiao_agg: DataFrame) -> None:
        """
        Visualiza e salva gráficos de vendas por região.

        Args:
            vendas_regiao_agg (DataFrame): Dados agregados de vendas agrupados por região.
        """
        # Ordenar regiões pelo total de vendas (decrescente)
        vendas_regiao_agg = vendas_regiao_agg.sort_values(by="VENDA_PECAS", ascending=False)

        # Top 10 regiões com mais vendas
        plt.figure(figsize=(10, 6))
        plt.bar(
            vendas_regiao_agg["CIDADE"][:10],
            vendas_regiao_agg["VENDA_PECAS"][:10],
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
        vendas_regiao_agg = vendas_regiao_agg.sort_values(by="VENDA_PECAS", ascending=True)
        plt.figure(figsize=(10, 6))
        plt.bar(
            vendas_regiao_agg["CIDADE"][-10:],
            vendas_regiao_agg["VENDA_PECAS"][-10:],
            color="salmon",
        )
        plt.title("Top 10 Regiões com Menos Vendas")
        plt.xlabel("Cidade")
        plt.ylabel("Vendas (Peças)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_regioes_com_menos_vendas.png"))
        plt.close()

    def plot_sales_velocity(self, velocity_data: DataFrame) -> None:
        """
        Visualiza e salva os 10 principais produtos por velocidade de venda.

        Args:
            velocity_data (DataFrame): Dados de velocidade de vendas.
        """
        # Agrupar e ordenar por velocidade de vendas
        velocity_by_product = (
            velocity_data.groupby(["PRODUTO", "COR_PRODUTO"]).agg({"VELOCIDADE_VENDA": "mean"}).reset_index()
        )
        velocity_by_product = velocity_by_product.sort_values(by="VELOCIDADE_VENDA", ascending=False)

        # Top 10 produtos por velocidade de vendas
        plt.figure(figsize=(10, 6))
        plt.bar(
            velocity_by_product["PRODUTO"][:10],
            velocity_by_product["VELOCIDADE_VENDA"][:10],
            color="lightgreen",
        )
        plt.title("Top 10 Produtos com Maior Velocidade de Venda")
        plt.xlabel("Produto")
        plt.ylabel("Velocidade de Venda")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "top_10_produtos_maior_velocidade_venda.png"))
        plt.close()

    def plot_sales_by_group(self, sales_data: DataFrame, vendas_df: DataFrame) -> None:
        """
        Visualiza e salva gráficos de vendas por produto e filial.

        Args:
            sales_data (DataFrame): Dados de velocidade de vendas.
            vendas_df (DataFrame): Dados de vendas.
        """
        # Vendas por produto
        vendas_por_produto = vendas_df.groupby(["PRODUTO"]).agg({"VENDA_PECAS": "sum"}).reset_index()
        plt.figure(figsize=(12, 8))
        plt.bar(
            vendas_por_produto["PRODUTO"],
            vendas_por_produto["VENDA_PECAS"],
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
        vendas_por_filial = vendas_df.groupby(["ID_FILIAL"]).agg({"VENDA_PECAS": "sum"}).reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(
            vendas_por_filial["ID_FILIAL"],
            vendas_por_filial["VENDA_PECAS"],
            color="purple",
        )
        plt.title("Vendas por Filial")
        plt.xlabel("Filial")
        plt.ylabel("Vendas (Peças)")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_directory, "vendas_por_filial.png"))
        plt.close()

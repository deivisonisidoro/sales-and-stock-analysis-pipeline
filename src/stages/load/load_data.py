from dataclasses import fields

import pandas as pd

from src.errors.load_error import LoadError
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.contracts.transform_contract import TransformContract


class LoadData:
    """
    Responsável pelo carregamento de dados transformados em um banco de dados.

    Esta classe é responsável por interagir com um repositório de banco de dados para
    inserir dados armazenados em DataFrames do pandas nas tabelas apropriadas do banco de dados.

    Atributos:
        __repository (DatabaseRepositoryInterface): Uma instância de uma interface de repositório de banco de dados
                                                    usada para interagir com o banco de dados.
    """

    def __init__(self, repository: DatabaseRepositoryInterface) -> None:
        """
        Inicializa a classe LoadData com um repositório especificado.

        Args:
            repository (DatabaseRepositoryInterface): O repositório de banco de dados usado para inserção de dados.
        """
        self.__repository = repository

    def load(self, data: TransformContract) -> None:
        """
        Carrega os dados no banco de dados iterando sobre os campos da classe TransformContract.

        Args:
            data (TransformContract): Um objeto contendo os DataFrames a serem inseridos.

        Raise:
            LoadError: Se ocorrer um erro durante o processo de carregamento.
        """
        if not isinstance(data, TransformContract):
            raise ValueError("Os dados devem ser uma instância de TransformContract.")

        # Verifica se algum DataFrame está vazio
        for field in fields(data):
            field_name = field.name
            field_value = getattr(data, field_name)
            if isinstance(field_value, pd.DataFrame) and field_value.empty:
                raise ValueError(f"O DataFrame para {field_name} está vazio.")
        try:
            self.create_table_if_not_exists()
            for field in fields(TransformContract):
                field_name = field.name
                field_value = getattr(data, field_name)
                if isinstance(field_value, pd.DataFrame):
                    self.__repository.insert_data(dataframe=field_value, table_name=field_name)
        except Exception as exception:
            raise LoadError(str(exception)) from exception

    def create_table_if_not_exists(self):
        create_stock_query = """
            CREATE TABLE IF NOT EXISTS stock (
                DATA_FOTO DATE NOT NULL,
                ID_FILIAL INT NOT NULL,
                PRODUTO VARCHAR(50) NOT NULL,
                COR_PRODUTO VARCHAR(50) NOT NULL,
                TAMANHO CHAR(50) NOT NULL,
                TOTAL INT NOT NULL,
                TRANSITO INT NOT NULL
            );
        """

        create_store_query = """
            CREATE TABLE IF NOT EXISTS store (
                ID_FILIAL INT NOT NULL,
                LOJA VARCHAR(100) NOT NULL,
                PONTO_VENDA_COD INT NOT NULL,
                PONTO_VENDA VARCHAR(200) NOT NULL,
                PUBLICO_LOJA CHAR(50) NOT NULL,
                CANAL VARCHAR(50) NOT NULL,
                CIDADE VARCHAR(100) NOT NULL,
                LOJA_M2 INT NOT NULL,
                PAIS CHAR(2) NOT NULL,
                UF CHAR(2) NOT NULL,
                CLIMA VARCHAR(50) NOT NULL,
                STATUS VARCHAR(20) NOT NULL
            );
        """
        create_products_query = """
            CREATE TABLE IF NOT EXISTS products (
                ARTIGO_COR VARCHAR(50) NOT NULL,
                ARTIGO VARCHAR(50) NOT NULL,
                DESC_PRODUTO VARCHAR(200) NOT NULL,
                COR VARCHAR(50),
                COR_DESCRICAO VARCHAR(200),
                NEGOCIO VARCHAR(100),
                PARTE VARCHAR(100),
                GRUPO VARCHAR(100),
                GENERO VARCHAR(50),
                COD_COTA INT,
                COLECAO VARCHAR(50),
                PIRAMIDE VARCHAR(50)
            );
        """

        create_sales_query = """
            CREATE TABLE IF NOT EXISTS sales (
                DATA_VENDA DATE NOT NULL,
                ID_FILIAL INT NOT NULL,
                PRODUTO VARCHAR(50) NOT NULL,
                COR_PRODUTO VARCHAR(50),
                TAMANHO VARCHAR(10),
                VENDA_PECAS INT,
                VENDA_LIQUIDA DECIMAL(10, 2),
                VENDA_BRUTA DECIMAL(10, 2)
            );
        """
        create_available_stock_query = """
            CREATE TABLE IF NOT EXISTS available_stock (
                PRODUTO VARCHAR(255),
                COR_PRODUTO VARCHAR(255),
                ESTOQUE_DISPONIVEL INT
            );
        """

        create_sales_velocity_query = """
            CREATE TABLE IF NOT EXISTS sales_velocity (
                DATA_VENDA DATE,
                ID_FILIAL INT,
                PRODUTO VARCHAR(255),
                COR_PRODUTO VARCHAR(255),
                TAMANHO VARCHAR(255),
                VENDA_PECAS INT,
                VENDA_LIQUIDA NUMERIC,
                VENDA_BRUTA NUMERIC,
                ESTOQUE_DISPONIVEL INT,
                VELOCIDADE_VENDA DECIMAL
            );
        """

        create_sales_by_region_query = """
            CREATE TABLE IF NOT EXISTS sales_by_region (
                UF VARCHAR(2),
                CIDADE VARCHAR(255),
                VENDA_PECAS INT
            );
        """
        for query in [
            create_stock_query,
            create_store_query,
            create_products_query,
            create_sales_query,
            create_sales_by_region_query,
            create_sales_velocity_query,
            create_available_stock_query,
        ]:
            self.__repository.create_table(query)

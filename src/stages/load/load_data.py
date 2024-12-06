from http.cookiejar import LoadError
from typing import Dict

from pandas import DataFrame

from src.infra.interface.database_repository import DatabaseRepositoryInterface


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

    def load(self, data: Dict[str, DataFrame]) -> None:
        """
        Carrega os dados no banco de dados iterando sobre um dicionário de nomes de tabelas e DataFrames.

        Args:
            data (Dict[str, DataFrame]): Um dicionário onde as chaves são os nomes das tabelas e
                                         os valores são DataFrames do pandas contendo os dados a serem inseridos.

        Raise:
            LoadError: Se ocorrer um erro durante o processo de carregamento, um LoadError personalizado é levantado.
        """
        self.create_table_if_not_exists()
        try:
            for key, value in data.items():
                self.__repository.insert_data(dataframe=value, table_name=key)
        except Exception as exception:
            raise LoadError(str(exception)) from exception

    def create_table_if_not_exists(self):
        create_estoque_disponivel_query = """
            CREATE TABLE IF NOT EXISTS estoque_disponivel (
                PRODUTO VARCHAR(255),
                COR_PRODUTO VARCHAR(255),
                ESTOQUE_DISPONIVEL INT
            );
        """

        create_velocidade_venda_query = """
            CREATE TABLE IF NOT EXISTS velocidade_venda (
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

        create_vendas_por_regiao_query = """
            CREATE TABLE IF NOT EXISTS vendas_por_regiao (
                UF VARCHAR(2),
                CIDADE VARCHAR(255),
                VENDA_PECAS INT
            );
        """

        self.__repository.create_table(create_estoque_disponivel_query)
        self.__repository.create_table(create_velocidade_venda_query)
        self.__repository.create_table(create_vendas_por_regiao_query)

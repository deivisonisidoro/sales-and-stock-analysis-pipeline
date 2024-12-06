from abc import ABC, abstractmethod

import pandas as pd


class DatabaseRepositoryInterface(ABC):
    """
    Classe base abstrata para operações de repositório de banco de dados.

    Esta interface define métodos para criar tabelas no banco de dados e
    inserir dados nas tabelas, que devem ser implementados por qualquer
    subclasse concreta.

    Métodos:
        create_table(query: str) -> None:
            Garante que uma tabela no banco de dados exista, executando a consulta SQL fornecida.

        insert_data(dataframe: pd.DataFrame, table_name: str) -> None:
            Insere dados de um DataFrame pandas em uma tabela do banco de dados especificada.
    """

    @abstractmethod
    def create_table(self, query: str) -> None:
        """
        Garante que uma tabela no banco de dados exista, executando a consulta SQL fornecida.

        Args:
            query (str): A consulta SQL para criar a tabela, caso ela não exista.
        """
        pass

    @abstractmethod
    def insert_data(self, dataframe: pd.DataFrame, table_name: str) -> None:
        """
        Insere dados de um DataFrame pandas na tabela especificada no banco de dados.

        Args:
            dataframe (pd.DataFrame): O DataFrame contendo os dados a serem inseridos.
            table_name (str): O nome da tabela no banco de dados onde os dados serão inseridos.
        """
        pass
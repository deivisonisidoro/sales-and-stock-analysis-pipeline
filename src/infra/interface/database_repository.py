from abc import ABC, abstractmethod

import pandas as pd


class DatabaseRepositoryInterface(ABC):
    """
    Classe base abstrata para operações de repositório de banco de dados.

    Esta interface define os métodos essenciais para a interação com o banco de dados,
    como criar tabelas, inserir dados e consultar registros. Deve ser implementada
    por subclasses concretas que realizem operações reais de banco de dados.

    Métodos:
        execute_query(query: str) -> None:
            Executa uma consulta SQL para criar uma tabela no banco de dados.

        insert_data(dataframe: pd.DataFrame, table_name: str) -> None:
            Insere os dados de um DataFrame pandas em uma tabela do banco de dados.

        find(table_name: str) -> pd.DataFrame:
            Retorna todos os registros de uma tabela específica como um DataFrame.
    """

    @abstractmethod
    def create(self, query: str) -> pd.DataFrame:
        """
        Cria uma tabela no banco de dados, se ela ainda não existir.

        Executa a consulta SQL fornecida para criar a tabela. Se ocorrer um erro durante
        a execução, a transação é revertida e uma mensagem de erro é exibida.

        Args:
            query (str): A consulta SQL para criar a tabela.

        Raise:
            Exception: Se ocorrer um erro durante a execução da consulta,
                       a transação é revertida e uma mensagem de erro é registrada.

        Nota:
            Este método usa uma conexão compartilhada com o banco de dados da classe `DatabaseConnection`.
        """
        pass

    @abstractmethod
    def insert_data(self, dataframe: pd.DataFrame, table_name: str) -> None:
        """
        Insere dados de um DataFrame pandas na tabela especificada no banco de dados.

        Args:
            dataframe (pd.DataFrame): O DataFrame contendo os dados que serão inseridos.
            table_name (str): O nome da tabela no banco de dados onde os dados serão armazenados.

        Raises:
            NotImplementedError: Se o método não for implementado em uma subclasse concreta.
        """
        pass

    @abstractmethod
    def find(self, query: str) -> pd.DataFrame:
        """
        Executa uma consulta SQL e retorna os registros resultantes como um DataFrame pandas.

        Este método é flexível e pode ser usado para:
            - Recuperar todos os registros de uma tabela específica.
            - Executar consultas SQL mais complexas para gerar relatórios personalizados.

        Args:
            query (str): A consulta SQL a ser executada. Pode ser uma consulta simples
            (e.g., `SELECT * FROM table_name`) ou uma consulta mais elaborada para relatórios.

        Returns:
            pd.DataFrame: Um DataFrame contendo os registros retornados pela consulta.

        Raises:
            NotImplementedError: Se o método não for implementado em uma subclasse concreta.
        """
        pass

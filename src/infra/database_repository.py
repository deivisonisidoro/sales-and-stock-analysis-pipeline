import pandas as pd
from psycopg2.extras import execute_values

from .database_connector import DatabaseConnection
from .interface.database_repository import DatabaseRepositoryInterface


class DatabaseRepository(DatabaseRepositoryInterface):
    """
    Implementa a interface `DatabaseRepositoryInterface` para interações com o banco de dados.

    Esta classe fornece métodos para criar tabelas e inserir dados no banco de dados,
    aproveitando uma conexão compartilhada com o banco de dados.
    """

    @classmethod
    def create(cls, query: str) -> None:
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
        cursor = DatabaseConnection.connection.cursor()
        try:
            cursor.execute(query)
            DatabaseConnection.connection.commit()
            print("Tabela criada com sucesso!")
        except Exception as e:
            DatabaseConnection.connection.rollback()
            print(f"Erro ao criar a tabela: {e}")
        finally:
            cursor.close()

    def insert_data(self, dataframe, table_name) -> None:
        """
        Insere dados de um DataFrame na tabela especificada no banco de dados.

        Transforma o DataFrame em tuplas e utiliza o método `execute_values` para inserção em massa.
        Se ocorrer um erro durante o processo de inserção, a transação é revertida,
        e uma mensagem de erro é exibida.

        Args:
            dataframe (pd.DataFrame): O DataFrame pandas contendo os dados a serem inseridos.
            table_name (str): O nome da tabela onde os dados devem ser inseridos.

        Raise:
            Exception: Se ocorrer um erro durante a inserção de dados,
                       a transação é revertida e uma mensagem de erro é registrada.

        Nota:
            - As colunas do DataFrame são usadas como os nomes das colunas da tabela.
            - Este método usa uma conexão compartilhada com o banco de dados da classe `DatabaseConnection`.
        """
        cursor = DatabaseConnection.connection.cursor()
        try:
            rows = [tuple(row) for row in dataframe.to_numpy()]
            columns = ", ".join(dataframe.columns)

            query = f"INSERT INTO {table_name} ({columns}) VALUES %s"
            execute_values(cursor, query, rows)
            DatabaseConnection.connection.commit()
            print(f"Dados carregados com sucesso na tabela {table_name}.")
        except Exception as e:
            DatabaseConnection.connection.rollback()
            print(f"Erro ao carregar dados na tabela {table_name}: {e}")
            raise Exception("Erro ao carregar dados na tabela") from e
        finally:
            cursor.close()

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
            Exception: Se ocorrer algum erro durante a execução da consulta.
        """
        cursor = DatabaseConnection.connection.cursor()
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(records, columns=columns)
            return df
        except Exception as e:
            raise Exception(f"Erro ao executar a consulta SQL: {e}") from e
        finally:
            cursor.close()

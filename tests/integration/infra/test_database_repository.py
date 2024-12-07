import pandas as pd
import psycopg2
import pytest

from src.infra.database_connector import DatabaseConnection
from src.infra.database_repository import DatabaseRepository


@pytest.fixture(scope="function")
def setup_database_connection(setup_test_database):
    """
    Fixture to set up a connection for the tests using the test database.
    """
    config = setup_test_database
    DatabaseConnection.connection = psycopg2.connect(
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    )
    yield DatabaseConnection.connection
    DatabaseConnection.connection.close()


def test_create_table(setup_database_connection):
    """
    Test the `create_table` method of `DatabaseRepository`.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """

    DatabaseRepository.create_table(create_table_query)

    # Verify the table was created
    with setup_database_connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'test_table'")
        result = cursor.fetchone()
    assert result is not None, "Table 'test_table' was not created."


def test_insert_data(setup_database_connection):
    """
    Test the `insert_data` method of `DatabaseRepository`.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """
    DatabaseRepository.create_table(create_table_query)

    # Prepare sample data
    data = {"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
    dataframe = pd.DataFrame(data)

    # Insert data into the table
    DatabaseRepository().insert_data(dataframe, "test_table")

    # Verify the data was inserted
    with setup_database_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]

    assert count == len(data["name"]), "Data was not inserted correctly."


def test_insert_data_handles_exceptions(setup_database_connection):
    """
    Test that `insert_data` handles exceptions correctly.
    """
    # Criação da tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """
    DatabaseRepository.create_table(create_table_query)

    # Prepare um DataFrame inválido
    data = {"name": ["Alice", "Bob", "Charlie"]}  # Coluna 'age' ausente
    dataframe = pd.DataFrame(data)

    # Verifique se a exceção correta é lançada
    with pytest.raises(Exception, match="Erro ao carregar dados na tabela"):
        DatabaseRepository().insert_data(dataframe, "test_table")

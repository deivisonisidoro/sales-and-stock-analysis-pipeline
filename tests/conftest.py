from typing import Generator

import psycopg2
import pytest
from psycopg2.sql import SQL, Identifier

from tests.config.settings import TEST_DATABASE_CONFIG


@pytest.fixture(scope="function")
def setup_test_database() -> Generator[dict[str, str], None, None]:
    """
    Fixture para configurar e desmontar um banco de dados de teste para testes de integração.

    Estabelece uma conexão com o servidor PostgreSQL, cria um banco de dados de teste,
    e o desmonta após a execução do teste.

    Yield:
        Generator[dict[str, str], None, None]: Configuração do banco de dados de teste.

    Exceções:
        pytest.fail: Se o processo de configuração do banco de dados encontrar um OperationalError.
    """
    admin_connection: psycopg2.extensions.connection | None = None
    cursor: psycopg2.extensions.cursor | None = None
    try:
        admin_connection = psycopg2.connect(
            dbname="postgres",
            user=TEST_DATABASE_CONFIG["user"],
            password=TEST_DATABASE_CONFIG["password"],
            host=TEST_DATABASE_CONFIG["host"],
            port=TEST_DATABASE_CONFIG["port"],
        )
        admin_connection.autocommit = True
        cursor = admin_connection.cursor()
        cursor.execute(SQL("CREATE DATABASE {}").format(Identifier(TEST_DATABASE_CONFIG["dbname"])))
        yield TEST_DATABASE_CONFIG
    except psycopg2.OperationalError as e:
        pytest.fail(f"Falha na configuração do banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if admin_connection:
            admin_connection.autocommit = True
            drop_connection = admin_connection.cursor()
            drop_connection.execute(
                SQL("DROP DATABASE IF EXISTS {}").format(Identifier(TEST_DATABASE_CONFIG["dbname"]))
            )
            drop_connection.close()
            admin_connection.close()

from typing import Generator

import psycopg2
import pytest
from psycopg2.sql import SQL, Identifier

from tests.config.settings import TEST_DATABASE_CONFIG


@pytest.fixture(scope="function")
def setup_test_database() -> Generator[dict[str, str], None, None]:
    """
    Fixture to setup and teardown a test database for integration tests.

    Yields:
        dict: Test database configuration.

    Exceptions:
        pytest.fail: If the database setup encounters an OperationalError.
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

        # Terminate active connections to the database if any
        cursor.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s",
            (TEST_DATABASE_CONFIG["dbname"],),
        )

        # Drop the database if it exists and create a new one
        cursor.execute(SQL("DROP DATABASE IF EXISTS {}").format(Identifier(TEST_DATABASE_CONFIG["dbname"])))
        cursor.execute(SQL("CREATE DATABASE {}").format(Identifier(TEST_DATABASE_CONFIG["dbname"])))
        yield TEST_DATABASE_CONFIG

    except psycopg2.OperationalError as e:
        pytest.fail(f"Database setup failed: {e}")
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

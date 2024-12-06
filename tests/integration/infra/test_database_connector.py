import psycopg2

from src.infra.database_connector import DatabaseConnection


def test_database_connection(setup_test_database: dict[str, str], monkeypatch) -> None:
    """
    Teste de integração para a classe DatabaseConnection.

    Valida que uma conexão com o banco de dados de teste pode ser estabelecida,
    verifica se a conexão está aberta, executa uma consulta simples e valida o resultado.

    Args:
        setup_test_database (dict[str, str]): Fixture que fornece a configuração do banco de dados de teste.
        monkeypatch (pytest.MonkeyPatch): Usado para modificar temporariamente a configuração do banco de dados.

    Exceções:
        AssertionError: Se a conexão ou a validação da consulta falharem.
    """
    monkeypatch.setattr("src.config.settings.DATABASE_CONFIG", setup_test_database)
    connection: psycopg2.extensions.connection = DatabaseConnection.connect()
    assert connection is not None
    assert connection.closed == 0
    cursor: psycopg2.extensions.cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    result: tuple[int] = cursor.fetchone()
    assert result[0] == 1
    cursor.close()
    connection.close()

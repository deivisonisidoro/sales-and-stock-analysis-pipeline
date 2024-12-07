from unittest.mock import patch

import pytest
from psycopg2 import OperationalError

from src.infra.database_connector import DatabaseConnection


def test_connect_successful():
    with patch.object(DatabaseConnection, "connect", return_value="Fake Connection"):
        conn = DatabaseConnection.connect()
        DatabaseConnection.connection = "Fake Connection"
        assert conn == "Fake Connection"
        assert DatabaseConnection.connection == "Fake Connection"


def test_connect_failure():
    with patch("psycopg2.connect", side_effect=OperationalError("Erro ao conectar")):
        with pytest.raises(Exception, match="Erro ao conectar-se ao banco de dados"):
            DatabaseConnection.connect()

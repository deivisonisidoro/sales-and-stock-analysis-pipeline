import psycopg2

from src.config.settings import DATABASE_CONFIG


class DatabaseConnection:
    """
    Uma classe para gerenciar a conexão com um banco de dados PostgreSQL usando psycopg2.

    A classe fornece métodos para estabelecer e gerenciar uma conexão com o banco de dados.
    Ela utiliza variáveis de ambiente para configurar os parâmetros de conexão.

    Atributos:
        connection (psycopg2.connection, opcional): Um objeto de conexão com o banco de dados PostgreSQL.
    """

    connection = None

    @classmethod
    def connect(cls):
        """
        Estabelece uma conexão com o banco de dados PostgreSQL usando a configuração
        especificada nas variáveis de ambiente.

        Variáveis de ambiente (carregadas de um arquivo .env) que devem ser definidas:
            - dbname: O nome do banco de dados para conectar.
            - user: O nome de usuário para autenticação.
            - password: A senha para o usuário especificado.
            - host: O host onde o servidor de banco de dados está localizado.
            - port: A porta em que o servidor de banco de dados está ouvindo.

        Retorna:
            conn (psycopg2.connection): O objeto de conexão com o banco de dados PostgreSQL.

        Raise:
            psycopg2.OperationalError: Se ocorrer um erro ao conectar-se ao banco de dados.
        """
        try:
            db_connection = psycopg2.connect(
                dbname=DATABASE_CONFIG.get("dbname"),
                user=DATABASE_CONFIG.get("user"),
                password=DATABASE_CONFIG.get("password"),
                host=DATABASE_CONFIG.get("host"),
                port=DATABASE_CONFIG.get("port"),
            )
            cls.connection = db_connection
            return db_connection
        except psycopg2.OperationalError as error:
            raise Exception(f"Erro ao conectar-se ao banco de dados: {error}")

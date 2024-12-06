import os

from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_CONFIG = {
    "dbname": os.getenv("TEST_POSTGRES_DB"),
    "user": os.getenv("TEST_POSTGRES_USER"),
    "password": os.getenv("TEST_POSTGRES_PASSWORD"),
    "host": os.getenv("TEST_DB_HOST"),
    "port": os.getenv("TEST_DB_PORT"),
}

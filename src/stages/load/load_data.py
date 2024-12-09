import os
from dataclasses import fields

import pandas as pd

from src.errors.load_error import LoadError
from src.infra.interface.database_repository import DatabaseRepositoryInterface
from src.stages.contracts.transform_contract import TransformContract


class LoadData:
    """
    Responsável pelo carregamento de dados transformados em um banco de dados.

    Esta classe é responsável por interagir com um repositório de banco de dados para
    inserir dados armazenados em DataFrames do pandas nas tabelas apropriadas do banco de dados.

    Atributos:
        __repository (DatabaseRepositoryInterface): Uma instância de uma interface de repositório de banco de dados
                                                    usada para interagir com o banco de dados.
    """

    def __init__(self, repository: DatabaseRepositoryInterface) -> None:
        """
        Inicializa a classe LoadData com um repositório especificado.

        Args:
            repository (DatabaseRepositoryInterface): O repositório de banco de dados usado para inserção de dados.
        """
        self.__repository = repository

    def load(self, data: TransformContract) -> None:
        """
        Carrega os dados no banco de dados iterando sobre os campos da classe TransformContract.

        Args:
            data (TransformContract): Um objeto contendo os DataFrames a serem inseridos.

        Raise:
            LoadError: Se ocorrer um erro durante o processo de carregamento.
        """
        if not isinstance(data, TransformContract):
            raise ValueError("Os dados devem ser uma instância de TransformContract.")

        # Verifica se algum DataFrame está vazio
        for field in fields(data):
            field_name = field.name
            field_value = getattr(data, field_name)
            if isinstance(field_value, pd.DataFrame) and field_value.empty:
                raise ValueError(f"O DataFrame para {field_name} está vazio.")
        try:
            self.create_table_if_not_exists()
            for field in fields(TransformContract):
                field_name = field.name
                field_value = getattr(data, field_name)
                if isinstance(field_value, pd.DataFrame):
                    self.__repository.insert_data(dataframe=field_value, table_name=field_name)
        except Exception as exception:
            raise LoadError(str(exception)) from exception

    def create_table_if_not_exists(self):
        # Listar todos os arquivos .sql na pasta de queries
        queries_dir = "src/queries/create"

        if not os.path.exists(queries_dir):
            print(f"A pasta {queries_dir} não foi encontrada!")
            return

        for filename in os.listdir(queries_dir):
            if filename.endswith(".sql"):
                file_path = os.path.join(queries_dir, filename)

                with open(file_path, "r") as file:
                    query = file.read()

                self.__repository.execute_query(query)

from pathlib import Path
from typing import Dict

import pandas as pd

from src.driver.interface.dataloader_interface import DataLoaderInterface


class DataLoader(DataLoaderInterface):
    """Implementação da DataLoaderInterface para manipulação de arquivos CSV."""

    def __init__(self, base_path: str = "data"):
        """Inicializa o carregador de dados com um caminho base para os arquivos CSV.

        Args:
            base_path (str): O diretório onde os arquivos CSV estão localizados. O padrão é "data".

        Raises:
            FileNotFoundError: Se o diretório especificado não existir.
        """
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {self.base_path}")

    def load_csv(self, file_name: str) -> pd.DataFrame:
        """Carrega um arquivo CSV em um DataFrame do pandas.

        Args:
            file_name (str): O nome do arquivo CSV a ser carregado.

        Returns:
            pd.DataFrame: Os dados carregados como um DataFrame.

        Raises:
            FileNotFoundError: Se o arquivo especificado não existir.
        """
        file_path = self.base_path / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        return pd.read_csv(file_path)

    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Carrega múltiplos arquivos CSV predefinidos em DataFrames do pandas.

        Os arquivos a serem carregados são predefinidos e incluem:
            - estoque_hering.csv
            - lojas_hering.csv
            - produtos_hering.csv
            - vendas_hering.csv

        Returns:
            Dict[str, pd.DataFrame]: Um dicionário onde as chaves são os nomes dos conjuntos de dados
            e os valores são os DataFrames correspondentes.
        """
        file_names = {
            "stock": "estoque_hering.csv",
            "store": "lojas_hering.csv",
            "products": "produtos_hering.csv",
            "sales": "vendas_hering.csv",
        }
        data = {}
        for key, file_name in file_names.items():
            data[key] = self.load_csv(file_name)
        return data

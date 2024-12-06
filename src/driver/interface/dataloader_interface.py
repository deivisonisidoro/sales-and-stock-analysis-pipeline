from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class DataLoaderInterface(ABC):
    """Interface para um carregador de dados."""

    @abstractmethod
    def load_csv(self, file_name: str) -> pd.DataFrame:
        """Carrega um arquivo CSV em um DataFrame do pandas.

        Args:
            file_name (str): O nome do arquivo CSV.

        Returns:
            pd.DataFrame: Os dados carregados como um DataFrame.
        """
        pass

    @abstractmethod
    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Carrega múltiplos arquivos CSV predefinidos em DataFrames do pandas.

        Returns:
            dict: Um dicionário onde as chaves são os nomes dos conjuntos de dados e os valores são os DataFrames.
        """
        pass

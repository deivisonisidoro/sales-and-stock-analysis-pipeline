import pandas as pd


class DataCleaner:
    """Responsável pelas operações de limpeza de dados."""

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa os dados removendo duplicatas e preenchendo valores ausentes.

        Args:
            df (pd.DataFrame): O DataFrame a ser limpo.

        Returns:
            pd.DataFrame: DataFrame limpo.
        """
        cleaned_df = df.drop_duplicates().fillna(0)
        return cleaned_df

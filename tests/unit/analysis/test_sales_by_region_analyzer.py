import pytest
from pandas import DataFrame

from src.analysis.analyze_data import SalesByRegionAnalyzer

sales_data = {"ID_FILIAL": [1, 2, 3, 4], "VENDA_PECAS": [100, 200, 150, 50]}

store_data = {
    "ID_FILIAL": [1, 2, 3, 4],
    "UF": ["SP", "RJ", "SP", "MG"],
    "CIDADE": ["São Paulo", "Rio de Janeiro", "Campinas", "Belo Horizonte"],
}


@pytest.fixture
def sales_df():
    """Fixture para o DataFrame de vendas."""
    return DataFrame(sales_data)


@pytest.fixture
def store_df():
    """Fixture para o DataFrame de lojas."""
    return DataFrame(store_data)


def test_calculate_sales_by_region(sales_df, store_df):
    """Testa a função calculate_sales_by_region da classe SalesByRegionAnalyzer."""

    result = SalesByRegionAnalyzer.calculate_sales_by_region(sales_df, store_df)

    assert isinstance(result, DataFrame), "O retorno deve ser um DataFrame"

    assert "UF" in result.columns, "A coluna 'UF' deveria estar no resultado"
    assert "CIDADE" in result.columns, "A coluna 'CIDADE' deveria estar no resultado"
    assert "VENDA_PECAS" in result.columns, "A coluna 'VENDA_PECAS' deveria estar no resultado"

    assert (
        result.loc[(result["UF"] == "SP") & (result["CIDADE"] == "São Paulo"), "VENDA_PECAS"].values[0] == 100
    ), "O valor de VENDA_PECAS está incorreto para São Paulo"
    assert (
        result.loc[(result["UF"] == "SP") & (result["CIDADE"] == "Campinas"), "VENDA_PECAS"].values[0] == 150
    ), "O valor de VENDA_PECAS está incorreto para Campinas"
    assert (
        result.loc[
            (result["UF"] == "RJ") & (result["CIDADE"] == "Rio de Janeiro"),
            "VENDA_PECAS",
        ].values[0]
        == 200
    ), "O valor de VENDA_PECAS está incorreto para Rio de Janeiro"
    assert (
        result.loc[
            (result["UF"] == "MG") & (result["CIDADE"] == "Belo Horizonte"),
            "VENDA_PECAS",
        ].values[0]
        == 50
    ), "O valor de VENDA_PECAS está incorreto para Belo Horizonte"


def test_empty_dataframes():
    """Testa a função calculate_sales_by_region com DataFrames vazios."""
    empty_sales_df = DataFrame(columns=["ID_FILIAL", "VENDA_PECAS"])
    empty_store_df = DataFrame(columns=["ID_FILIAL", "UF", "CIDADE"])

    result = SalesByRegionAnalyzer.calculate_sales_by_region(empty_sales_df, empty_store_df)

    assert result.empty, "O DataFrame resultante deveria estar vazio quando os dados de entrada forem vazios"

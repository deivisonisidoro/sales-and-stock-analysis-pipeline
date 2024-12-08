import pandas as pd
import pytest

from src.stages.contracts.extract_contract import ExtractContract
from src.stages.contracts.transform_contract import TransformContract
from src.stages.transform.transform_data import TransformData


@pytest.fixture
def mock_extract_contract():
    """Fixture to create a mocked ExtractContract with sample data."""
    stock_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "TOTAL": [100, 200],
            "TRANSITO": [10, 20],
        }
    )

    sales_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "VENDA_PECAS": [30, 50],
        }
    )

    products_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "DESCRICAO": ["Product A", "Product B"],
        }
    )

    store_data = pd.DataFrame(
        {
            "ID_FILIAL": [1, 2],
            "UF": ["SP", "RJ"],
            "CIDADE": ["São Paulo", "Rio de Janeiro"],
        }
    )

    return ExtractContract(
        stock=stock_data,
        sales=sales_data,
        store=store_data,
        products=products_data,
    )


def test_transform_success():
    """
    Test the transform method for successful data transformation.
    """
    # Mocked data
    sales_data = {
        "PRODUTO": ["A", "B"],
        "COR_PRODUTO": ["Red", "Blue"],
        "VENDA_PECAS": [30, 50],
        "ID_FILIAL": [1, 2],
    }
    stock_data = {
        "PRODUTO": ["A", "B"],
        "COR_PRODUTO": ["Red", "Blue"],
        "TOTAL": [100, 200],
        "TRANSITO": [10, 20],
    }
    store_data = {
        "ID_FILIAL": [1, 2],
        "UF": ["SP", "RJ"],
        "CIDADE": ["São Paulo", "Rio de Janeiro"],
    }
    products_data = {
        "PRODUTO": ["A", "B"],
        "DESCRICAO": ["Product A", "Product B"],
    }

    # Create mocked DataFrames
    sales_df = pd.DataFrame(sales_data)
    stock_df = pd.DataFrame(stock_data)
    store_df = pd.DataFrame(store_data)
    products_df = pd.DataFrame(products_data)

    # Mocked extract contract
    mock_extract_contract = ExtractContract(sales=sales_df, stock=stock_df, store=store_df, products=products_df)

    # Execute the service
    service = TransformData()
    result = service.transform(mock_extract_contract)

    # Assertions
    assert isinstance(result, TransformContract)
    assert not result.sales_velocity.empty
    assert not result.available_stock.empty
    assert not result.sales_by_region.empty
    assert result.store.equals(store_df)
    assert result.sales.equals(sales_df)

    # Validate stock transformations
    expected_stock_df = stock_df.copy()
    expected_stock_df["ESTOQUE_DISPONIVEL"] = expected_stock_df["TOTAL"] - expected_stock_df["TRANSITO"]

    pd.testing.assert_frame_equal(result.stock, expected_stock_df, check_dtype=False)


def test_clean_data():
    """
    Test the _clean_data method for cleaning the input DataFrame.
    """
    service = TransformData()
    input_data = pd.DataFrame({"Column1": [1, 2, 2], "Column2": [None, "Value", "Value"]})
    expected_output = pd.DataFrame({"Column1": [1, 2], "Column2": [0, "Value"]})

    cleaned_data = service._clean_data(input_data)

    pd.testing.assert_frame_equal(cleaned_data, expected_output)


def test_calculate_available_stock():
    """
    Test the _calculate_available_stock method for correct stock calculation.
    """
    service = TransformData()
    stock_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "TOTAL": [100, 200],
            "TRANSITO": [10, 20],
        }
    )

    expected_output = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "ESTOQUE_DISPONIVEL": [90, 180],
        }
    )

    result = service._calculate_available_stock(stock_data)

    pd.testing.assert_frame_equal(result, expected_output)


def test_calculate_sales_velocity():
    """
    Test the _calculate_sales_velocity method for correct sales velocity calculation.
    """
    service = TransformData()
    sales_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "VENDA_PECAS": [30, 50],
        }
    )

    stock_data = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "ESTOQUE_DISPONIVEL": [90, 180],
        }
    )

    expected_output = pd.DataFrame(
        {
            "PRODUTO": ["A", "B"],
            "COR_PRODUTO": ["Red", "Blue"],
            "VENDA_PECAS": [30, 50],
            "ESTOQUE_DISPONIVEL": [90, 180],
            "VELOCIDADE_VENDA": [30 / 90, 50 / 180],
        }
    )

    result = service._calculate_sales_velocity(sales_data, stock_data)

    pd.testing.assert_frame_equal(result, expected_output)


def test_calculate_sales_by_region():
    """
    Test the _calculate_sales_by_region method for correct sales aggregation by region.
    """
    service = TransformData()
    sales_data = pd.DataFrame(
        {
            "ID_FILIAL": [1, 2],
            "VENDA_PECAS": [30, 50],
        }
    )

    store_data = pd.DataFrame(
        {
            "ID_FILIAL": [1, 2],
            "UF": ["SP", "RJ"],
            "CIDADE": ["São Paulo", "Rio de Janeiro"],
        }
    )

    expected_output = pd.DataFrame(
        {
            "UF": ["RJ", "SP"],
            "CIDADE": ["Rio de Janeiro", "São Paulo"],
            "VENDA_PECAS": [50, 30],
        }
    )

    result = service._calculate_sales_by_region(sales_data, store_data)

    pd.testing.assert_frame_equal(result, expected_output)

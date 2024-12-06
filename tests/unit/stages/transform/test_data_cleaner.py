import pandas as pd

from src.stages.transform.data_cleaner import DataCleaner


def test_clean_data_remove_duplicates():
    """Testa se o método clean_data remove duplicatas corretamente."""

    data = {"col1": [1, 1, 2, 3], "col2": [4, 4, 5, 6]}
    df = pd.DataFrame(data)

    cleaned_df = DataCleaner.clean_data(df)

    expected_data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    expected_df = pd.DataFrame(expected_data)

    cleaned_df.reset_index(drop=True, inplace=True)
    expected_df.reset_index(drop=True, inplace=True)

    pd.testing.assert_frame_equal(cleaned_df, expected_df)


def test_clean_data_fill_na():
    """Testa se o método clean_data preenche valores ausentes corretamente com 0."""

    data = {"col1": [1, 2, None, 3], "col2": [None, 5, 6, 7]}
    df = pd.DataFrame(data)

    cleaned_df = DataCleaner.clean_data(df)

    expected_data = {"col1": [1, 2, 0, 3], "col2": [0, 5, 6, 7]}
    expected_df = pd.DataFrame(expected_data)

    cleaned_df["col1"] = cleaned_df["col1"].astype("int64")
    cleaned_df["col2"] = cleaned_df["col2"].astype("int64")  # Forçando a conversão para int64 também em col2
    expected_df["col1"] = expected_df["col1"].astype("int64")
    expected_df["col2"] = expected_df["col2"].astype("int64")  # Garantindo que o tipo seja igual para col2

    pd.testing.assert_frame_equal(cleaned_df, expected_df)


def test_clean_data_no_change():
    """Testa se o método clean_data não altera o DataFrame quando não há duplicatas nem valores ausentes."""

    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    df = pd.DataFrame(data)

    cleaned_df = DataCleaner.clean_data(df)

    pd.testing.assert_frame_equal(df, cleaned_df)

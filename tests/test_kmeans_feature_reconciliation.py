import pandas as pd

from backend.predict import align_features_to_model


def test_align_features_to_model_keeps_expected_schema():
    expected = ["a", "b", "c", "d"]
    df = pd.DataFrame({
        "x": [1, 2],
        "a": [3, 4],
        "z": [9, 8],
        "b": [5, 6],
        "c": [7, 8],
        "d": [9, 10],
    })

    result = align_features_to_model(df, expected)

    assert list(result.columns) == expected
    assert result.shape[1] == len(expected)

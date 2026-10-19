from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from backend.constants import (
    KMEANS_RETRAINED_V3_TXT_PATH,
    KMEANS_TXT_PATH,
    UNSUPERVISED_MODEL_PATHS,
)
from backend.del_columns import del_columns, elimina
from backend.model_utils import dict_predict
from backend.legacy_del_columns import del_columns as legacy_del_columns
from backend.predict import predecir
import metricas


class DummyAnomalyModel:
    def decision_function(self, data):
        return np.array([-0.8, 0.7])

    def predict(self, data):
        return np.array([-1, 1])


@pytest.mark.parametrize("model_option", ["IForest", "OCSVM"])
def test_anomaly_models_use_inverted_artifact_polarity(model_option):
    _, predictions, scores = predecir(
        DummyAnomalyModel(),
        pd.DataFrame({"feature": [1.0, 2.0]}),
        model_option,
    )

    np.testing.assert_array_equal(predictions, [0, 1])
    np.testing.assert_array_equal(scores, [-0.8, 0.7])


def test_iforest_uses_threshold_saved_with_retrained_model():
    _, predictions, scores = predecir(
        {"modelo": DummyAnomalyModel(), "umbral": -0.05},
        pd.DataFrame({"feature": [1.0, 2.0]}),
        "IForest",
    )

    np.testing.assert_array_equal(predictions, [0, 1])
    np.testing.assert_array_equal(scores, [-0.8, 0.7])


def test_unsupervised_models_point_to_new_artifacts_and_keep_old_artifacts():
    expected_active_artifacts = {
        "IForest": "iforest__EJERCICIO10_n_components6_fit.pkl",
        "OCSVM": "ocsvm_reentrenado_v2.pkl",
        "KMEANS": "kmeans1__EJERCICIO10_n_components6_over.pkl",
        "AUTOENCODER": "autoencoder_reentrenado_v2.pkl",
    }
    inactive_artifacts = [
        "model/iforest_reentrenado_v2.pkl",
        "model/ocsvm__EJERCICIO10_n_components6_fit.pkl",
        "model/kmeans_reentrenado_v3.pkl",
        "model/autoencoder.pkl",
    ]

    for model_name, filename in expected_active_artifacts.items():
        assert Path(UNSUPERVISED_MODEL_PATHS[model_name]).name == filename
        assert Path(UNSUPERVISED_MODEL_PATHS[model_name]).is_file()

    assert all(Path(path).is_file() for path in inactive_artifacts)


def test_del_columns_matches_retrained_model_feature_list():
    columns = elimina + ["number__icmp_type", "retained_feature"]
    data = pd.DataFrame([[1] * len(columns)], columns=columns)

    result = del_columns(columns).fit_transform(data)

    assert list(result.columns) == ["number__icmp_type", "retained_feature"]

    legacy_result = legacy_del_columns(columns).fit_transform(data)
    assert list(legacy_result.columns) == ["retained_feature"]


def test_clean_capture_kmeans_clusters_are_mapped_as_normal():
    mapping = dict_predict(KMEANS_RETRAINED_V3_TXT_PATH)

    for cluster in [1, 9, 17, 18, 23, 35]:
        assert mapping[cluster] == "Normal"


def test_original_kmeans_mapping_matches_original_cluster_count():
    mapping = dict_predict(KMEANS_TXT_PATH)

    assert sorted(mapping) == list(range(29))


def test_model_predictions_are_not_candidates_for_ground_truth_labels():
    data = pd.DataFrame({
        "label": ["Normal", "Attack", "Normal"],
        "prediccion_id": [0, 1, 0],
        "prediccion_binaria": [0, 1, 0],
        "prediccion": ["Normal", "Attack", "Normal"],
        "modelo_prediccion": ["RandomForest"] * 3,
        "prediction": [0, 1, 0],
        "prediction_id": [0, 1, 0],
        "prediction_binary": [0, 1, 0],
        "model_prediction": ["RandomForest"] * 3,
    })

    assert metricas.candidate_label_columns(data) == ["label"]

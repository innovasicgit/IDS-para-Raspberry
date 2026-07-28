import ast
import os
import sys
import joblib
import numpy as np
import pandas as pd
from collections import Counter
from pathlib import Path

import streamlit as st

from .constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH,
)

# Importar la clase del_columns necesaria para cargar los modelos serializados
try:
    # Primero intentar importar desde backend
    from .del_columns import del_columns
except ImportError:
    try:
        # Si falla, intentar desde el directorio raíz
        root_dir = str(Path(__file__).parent.parent)
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
        from del_columns import del_columns
    except ImportError:
        st.warning("No se pudo importar del_columns. Algunos modelos podrían no cargar correctamente.")
        # Definir una clase dummy para evitar errores
        from sklearn.base import BaseEstimator, TransformerMixin
        class del_columns(BaseEstimator, TransformerMixin):
            def __init__(self, columns):
                self.columns = columns
            def fit(self, X, y=None):
                return self
            def transform(self, X, y=None):
                return X


@st.cache_resource(show_spinner="Cargando modelo...")
def load_model(model_path):
    """Carga un modelo desde disco y lo cachea en memoria (solo se carga 1 vez)."""
    try:
        absolute_path = os.path.abspath(model_path)
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"El archivo {absolute_path} no se encuentra.")
        
        model = joblib.load(absolute_path)
        
        # Verificar si el modelo está fitted
        from sklearn.utils.validation import check_is_fitted
        try:
            if hasattr(model, 'named_steps'):
                for name, step in model.named_steps.items():
                    check_is_fitted(step)
            else:
                check_is_fitted(model)
        except Exception as fit_error:
            pass  # No mostrar warnings en función cacheada
        
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        import traceback
        st.error(f"Detalles del error: {traceback.format_exc()}")
        return None


def dict_predict(path2):
    with open(path2, 'r') as f:
        raw = f.read()
    lista_tuplas = ast.literal_eval(raw)
    return dict(lista_tuplas)


def pred_threshold(score, threshold):
    score = pd.Series(score)
    Actual_pred = pd.DataFrame({'Pred': score})
    Actual_pred['Pred'] = np.where(Actual_pred['Pred'] <= threshold, 0, 1)
    return Actual_pred.reset_index(drop=True)


def dbscan_predict(model, X):
    """Predice etiquetas para nuevas muestras usando un modelo DBSCAN entrenado.

    Esta función se conserva por compatibilidad con código legacy que hace:
    `from backend.model_utils import dbscan_predict`.
    Si no hay suficientes atributos en el modelo, devuelve -1 (ruido) para todas.
    """
    X_arr = np.asarray(X)
    if X_arr.ndim == 1:
        X_arr = X_arr.reshape(1, -1)

    core = getattr(model, 'components_', None)
    core_labels = getattr(model, 'labels_', None)
    eps = float(getattr(model, 'eps', 0.5))

    if core is None or core_labels is None or len(core) == 0:
        return np.full(X_arr.shape[0], -1, dtype=int)

    y_new = np.full(X_arr.shape[0], -1, dtype=int)

    for i, x in enumerate(X_arr):
        dists = np.linalg.norm(core - x, axis=1)
        j = int(np.argmin(dists))
        if dists[j] <= eps:
            y_new[i] = int(core_labels[j])

    return y_new


 

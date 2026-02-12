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


def load_model(model_path):
    try:
        absolute_path = os.path.abspath(model_path)
        st.write(f"Intentando cargar desde: {absolute_path}")
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"El archivo {absolute_path} no se encuentra.")
        
        # Cargar el modelo con el contexto correcto
        model = joblib.load(absolute_path)
        st.write(f"Tipo del modelo cargado: {type(model)}")
        
        # Verificar si el modelo está fitted
        from sklearn.utils.validation import check_is_fitted
        try:
            if hasattr(model, 'named_steps'):
                for name, step in model.named_steps.items():
                    check_is_fitted(step)
            else:
                check_is_fitted(model)
            st.success("✓ Modelo cargado y verificado correctamente")
        except Exception as fit_error:
            st.warning(f"⚠ Advertencia: El modelo podría no estar entrenado correctamente: {fit_error}")
        
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


 

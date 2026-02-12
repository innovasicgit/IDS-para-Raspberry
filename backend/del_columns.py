"""
Transformador personalizado para eliminar columnas específicas del dataset.
Esta clase se usa en los pipelines de preprocesamiento de los modelos serializados.
"""

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


# Lista de columnas a eliminar durante el preprocesamiento
elimina = [
    'number__tcp_flags_cwr', 
    'number__tcp_flags_ecn', 
    'number__tcp_flags_urg', 
    'number__tcp_flags_ack',
    'number__tcp_flags_push', 
    'number__tcp_flags_reset',
    'number__tcp_flags_fin', 
    'number__icmp_type',
    'number__ip_flags_rb', 
    'number__tcp_flags_res'
]


class del_columns(BaseEstimator, TransformerMixin):
    """
    Transformador que elimina columnas específicas de un DataFrame.
    Compatible con pipelines de scikit-learn.
    """
    
    def __init__(self, columns):
        """
        Args:
            columns: Lista de nombres de columnas presentes en el dataset
        """
        self.columns = columns
        
    def fit(self, X, y=None):
        """
        No requiere entrenamiento. Solo retorna self para compatibilidad con pipelines.
        """
        return self
        
    def transform(self, X, y=None):
        """
        Transforma X eliminando las columnas especificadas en 'elimina'.
        
        Args:
            X: Array numpy o DataFrame a transformar
            y: Target (no usado)
            
        Returns:
            DataFrame con las columnas eliminadas
        """
        # Convertir a DataFrame si es necesario
        X = pd.DataFrame(X, columns=self.columns)
        
        # Eliminar columnas que existan en el DataFrame
        columnas_a_eliminar = [col for col in elimina if col in X.columns]
        X_ = X.drop(columnas_a_eliminar, axis=1)
        
        return X_
    
    def get_feature_names_out(self, input_features=None):
        """
        Retorna los nombres de las features después de la transformación.
        Método requerido por versiones recientes de scikit-learn.
        """
        if input_features is None:
            input_features = self.columns
        return [col for col in input_features if col not in elimina]

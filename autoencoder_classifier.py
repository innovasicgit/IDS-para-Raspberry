# autoencoder_classifier.py
# Módulo puente para compatibilidad con pickle/joblib.
# El modelo autoencoder.pkl fue serializado con este nombre de módulo,
# así que debe existir en la raíz del proyecto para que joblib.load() funcione.

from backend.autoencoderclassifier import AutoencoderClassifier

__all__ = ['AutoencoderClassifier']

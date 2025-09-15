import joblib
import pandas as pd
import numpy as np
from del_columns import del_columns
from autoencoder_classifier import AutoencoderClassifier


# Ahora intenta cargar el modelo
model_path = "model/autoencoder.pkl"
loaded_object = joblib.load(model_path)
print(f"Tipo del objeto cargado: {type(loaded_object)}")
print(f"Contenido: {loaded_object}")

print( "Este es el nombre de los pasos del pipeline" , loaded_object[0].named_steps.keys())

print(loaded_object[0].named_steps['prepro_2_del'].named_steps['prepro_1_num_cat'])

columns = loaded_object[0].named_steps['prepro_2_del']\
                  .named_steps['prepro_1_num_cat']\
                  .get_feature_names_out().tolist()
print("Columnas del pipeline: ", columns)

loaded_object[0].named_steps['prepro_2_del'].named_steps['del_columns'] = del_columns(columns)

import streamlit as st
from autoencoder_classifier import AutoencoderClassifier
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
from pyod.utils.utility import standardizer
from pyod.models.combination import average
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import sklearn
import sklearn.metrics as metrics
from sklearn.metrics import auc, silhouette_score, calinski_harabasz_score, davies_bouldin_score
from streamlit_option_menu import option_menu
import time
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from subprocess import PIPE, Popen
import shlex
import psutil
import os
import threading
import tempfile
import metricas
import pickle
from del_columns import del_columns
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from collections import Counter
import ast
from sklearn.metrics import DistanceMetric
import sklearn.metrics._dist_metrics as _dm
import numpy as np
from sklearn.neighbors import NearestNeighbors
import psutil
import GPUtil
import time


def load_model(model_path):
    try:
        # Cargar el modelo usando joblib
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        import traceback
        st.error(f"Detalles del error: {traceback.format_exc()}")
        return None

def dict_predict(path2):
    # Lee todo el contenido
    with open(path2, 'r') as f:
        raw = f.read()

    # Convierte la cadena a la lista de tuplas
    lista_tuplas = ast.literal_eval(raw)  # -> [(0, 'Normal'), (1, 'DDoS_TCP'), …]

    # Construye el dict de un paso
    dict_predict = dict(lista_tuplas)
    return dict_predict

def pred_threshold(
    score, threshold):
    score = pd.Series(score)  # ✅ Convertir a Series si es un array
    Actual_pred = pd.DataFrame({'Pred': score})  
    Actual_pred['Pred'] = np.where(Actual_pred['Pred']<=threshold,0,1)
    Actual_pred=Actual_pred.reset_index(drop=True)
    return (Actual_pred)

def dbscan_predict(dbscan, X_new):
    """
    Asigna cada punto de X_new al clúster del vecino core más cercano
    usando el DBSCAN ya entrenado.
    """
    # 1) Extrae los core samples y sus etiquetas
    core_samples = dbscan.components_
    core_labels  = dbscan.labels_[dbscan.core_sample_indices_]

    # 2) Ajusta un NearestNeighbors sobre esos core samples
    nn = NearestNeighbors(n_neighbors=1).fit(core_samples)

    # 3) Para cada punto nuevo, obtiene distancia y índice de vecino
    dist, idx = nn.kneighbors(X_new)

    # 4) Si la distancia <= eps, asigna la etiqueta de ese vecino; si no, -1
    return np.where(dist.ravel() <= dbscan.eps,
                    core_labels[idx.ravel()],
                    -1)

# IMPORTANTE: st.set_page_config debe ser la primera llamada a Streamlit en el script
st.set_page_config(
    page_title="Sistema IDS IoT - Detección de Intrusiones",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar animaciones Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        st.error(f"Error al cargar la animación desde {url}. Estado HTTP: {r.status_code}")
        return None
    return r.json()


#----------------------------------------------------  Estilos CSS --------------------------------------------------------------------------------------------------------------------------------
st.markdown("""
<style>
    body {
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    .mi-caja label {
        color: black !important;         /* etiqueta en negro */
    }
    .mi-caja input {
        color: black !important;         /* texto que se escribe en negro */
        background-color: white !important;
        caret-color: black !important;
    }

        .main-header {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(90deg, #1E3D59 0%, #2E5077 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .success-animation {
        animation: fadeInOut 3s forwards;
    }
    @keyframes fadeInOut {
        0% { opacity: 0; }
        20% { opacity: 1; }
        80% { opacity: 1; }
        100% { opacity: 0; display: none; }
    }
    .stAlert {
        background-color: rgba(25, 25, 25, 0.5);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 10px;
    }
    .stButton > button {
        background: rgba(255, 255, 255, 0.1);
        border: none;
        color: #ffffff;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0, 0, 0, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    .stButton > button:active {
        transform: translateY(1px);
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    .dashboard-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
    }
    .notification {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        animation: fadeOut 2s forwards;
        animation-delay: 3.5s;
    }
    @keyframes fadeOut {
        from {opacity: 1;}
        to {opacity: 0; height: 0; padding: 0; margin: 0;}
    }
    .streamlit-expanderHeader, .stTextInput > div > div > input {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    .stDataFrame {
        color: #ffffff;
    }
    .card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .carousel {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
    }
    .carousel-item {
        flex: none;
        scroll-snap-align: start;
        margin-right: 20px;
    }
    
""", unsafe_allow_html=True)

# ---------------------------------------------------- INICIO PAGE----------------------------------------------------------------------------------------------------------------------------
# Navegación mejorada
from pathlib import Path

with st.sidebar:
    logo_path = Path(__file__).parent / "img" / "logo.png"
    st.image(str(logo_path), width=150)
    selected = option_menu(
        "Navegación",
        ["Inicio", "Panel de Control"],
        icons=["house", "graph-up"],
        menu_icon="cast",
        default_index=0
    )

    st.session_state.page = "home" if selected == "Inicio" else "dashboard"

def show_home_page():
    # Hero Section con imagen principal
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1E3D59 0%, #2E5077 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🛡️ Sistema de Detección de Intrusiones para IoT
        </h1>
        <h3 style="color: #B8D4E3; font-weight: 300; margin-bottom: 2rem;">
            Protegiendo el futuro digital con inteligencia artificial avanzada
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Placeholder para imagen principal del sistema
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 3rem; 
                background: linear-gradient(45deg, #f0f2f6, #ffffff); 
                border-radius: 15px; border: 2px dashed #ddd;">
        <h4 style="color: #666; margin-bottom: 1rem;">📸 ESPACIO PARA IMAGEN PRINCIPAL</h4>
        <p style="color: #888;">Imagen del sistema IDS en funcionamiento o arquitectura de red IoT</p>
        <p style="color: #aaa; font-size: 0.9rem;">Dimensiones recomendadas: 800x400px</p>
    </div>
    """, unsafe_allow_html=True)

    # Descripción principal mejorada
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 2rem; border-radius: 15px; 
                border-left: 4px solid #4CAF50; margin: 2rem 0;">
        <p style="font-size: 1.2rem; line-height: 1.8; text-align: justify;">
            Bienvenido al <strong>Sistema de Detección de Intrusiones en Redes IoT</strong>, 
            una solución avanzada diseñada para monitorear y detectar anomalías 
            en redes de IoT, brindando seguridad y confiabilidad sin precedentes. 
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            Nuestro sistema utiliza modelos de vanguardia en detección de anomalías, como 
            <strong>IForest</strong> (Isolation Forest), <strong>OCSVM</strong> (One Class Support Vector Machine),
            <strong>K-MEANS</strong> y <strong>Autoencoder multiclase</strong> para analizar patrones complejos 
            y alertar sobre posibles irregularidades en la red en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de características principales con iconos
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
        🎯 Características Principales del Sistema
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="background: rgba(76, 175, 80, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 250px; 
                    border: 1px solid rgba(76, 175, 80, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h4 style="color: #4CAF50;">Detección en Tiempo Real</h4>
            <p style="font-size: 0.9rem;">Monitoreo continuo y análisis instantáneo de patrones de red</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="background: rgba(33, 150, 243, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 250px; 
                    border: 1px solid rgba(33, 150, 243, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h4 style="color: #2196F3;">IA Avanzada</h4>
            <p style="font-size: 0.9rem;">Algoritmos de machine learning de última generación</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="background: rgba(255, 152, 0, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 250px; 
                    border: 1px solid rgba(255, 152, 0, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #FF9800;">Análisis Predictivo</h4>
            <p style="font-size: 0.9rem;">Predicción de amenazas y comportamientos anómalos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card" style="background: rgba(244, 67, 54, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 250px; 
                    border: 1px solid rgba(244, 67, 54, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚫</div>
            <h4 style="color: #F44336;">Protección Activa</h4>
            <p style="font-size: 0.9rem;">Identificación y mitigación automática de amenazas</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Placeholder para imagen de arquitectura
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; 
                background: linear-gradient(45deg, #e3f2fd, #f3e5f5); 
                border-radius: 15px; border: 2px dashed #9c27b0;">
        <h4 style="color: #7b1fa2; margin-bottom: 1rem;">🏗️ ESPACIO PARA DIAGRAMA DE ARQUITECTURA</h4>
        <p style="color: #8e24aa;">Diagrama mostrando la arquitectura del sistema IDS</p>
        <p style="color: #ba68c8; font-size: 0.9rem;">Dimensiones recomendadas: 1000x500px</p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de interpretación de resultados mejorada
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #FF9800; margin: 3rem 0 2rem 0;">
        💬 Interpretación de Resultados
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.1); padding: 2rem; border-radius: 15px; 
                    border-left: 4px solid #4CAF50; height: 350px;">
            <h4 style="color: #4CAF50; text-align: center; margin-bottom: 1.5rem;">
                🟢 Métricas de Validación
            </h4>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Silhouette Score:</strong> Mide la calidad de los clusters (ideal > 0.5)
                </li>
                <li style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Calinski Score:</strong> Evalúa la separación entre clusters
                </li>
                <li style="padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Davies Score:</strong> Indica la similitud dentro de clusters
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(33, 150, 243, 0.1); padding: 2rem; border-radius: 15px; 
                    border-left: 4px solid #2196F3; height: 450px;">
            <h4 style="color: #2196F3; text-align: center; margin-bottom: 1.5rem;">
                🔰 Clasificación de Anomalías
            </h4>
            <div style="margin-bottom: 1rem; padding: 0.8rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <strong style="color: #4CAF50;">Normal:</strong> Tráfico de red esperado
            </div>
            <div style="margin-bottom: 1rem; padding: 0.8rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <strong style="color: #FF5252;">Anómalo:</strong> Patrones sospechosos
            </div>
            <div style="padding: 0.8rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <strong>Multiclase:</strong>
                <ul style="margin-top: 0.5rem; padding-left: 1rem;">
                    <li>DDoS_TCP</li>
                    <li>DDoS_UDP</li>
                    <li>Reconnaissance</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 152, 0, 0.1); padding: 2rem; border-radius: 15px; 
                    border-left: 4px solid #FF9800; height: 350px;">
            <h4 style="color: #FF9800; text-align: center; margin-bottom: 1.5rem;">
                📈 Métricas de Rendimiento
            </h4>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>CPU:</strong> % Consumo por segundo
                </li>
                <li style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Memoria:</strong> % Uso de RAM
                </li>
                <li style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Disco:</strong> % Uso de almacenamiento
                </li>
                <li style="padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <strong>Tiempo:</strong> Duración en segundos
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Placeholder para imagen comparativa de modelos
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; 
                background: linear-gradient(45deg, #fff3e0, #fce4ec); 
                border-radius: 15px; border: 2px dashed #e91e63;">
        <h4 style="color: #c2185b; margin-bottom: 1rem;">📊 ESPACIO PARA GRÁFICOS COMPARATIVOS</h4>
        <p style="color: #ad1457;">Comparación visual del rendimiento de diferentes modelos</p>
        <p style="color: #f06292; font-size: 0.9rem;">Dimensiones recomendadas: 1200x600px</p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de modelos mejorada
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #9C27B0; margin: 3rem 0 2rem 0;">
        🔎 Modelos de Detección de Anomalías
    </h2>
    """, unsafe_allow_html=True)
    
    # Grid de modelos con diseño mejorado
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🔵 OCSVM (One Class Support Vector Machine)", expanded=False):
            st.markdown("""
            <div style="background: rgba(63, 81, 181, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <p style="text-align: justify; line-height: 1.6;">
                El modelo OCSVM es un algoritmo de detección de anomalías basado en Support Vector Machine (SVM), 
                que funciona creando una frontera en el espacio de características que agrupa la mayor parte 
                de los datos de entrenamiento como normales y considera como anomalías aquellas muestras que 
                queden fuera de esta región.
                </p>
                <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <strong style="color: #4CAF50;">✅ Ventajas:</strong> Efectivo para datos de alta dimensionalidad
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🟠 K-means", expanded=False):
            st.markdown("""
            <div style="background: rgba(255, 152, 0, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <p style="text-align: justify; line-height: 1.6;">
                El modelo K-means es un algoritmo de agrupamiento que tiene como objetivo dividir un conjunto 
                de datos en grupos que sean lo más similares posible internamente y los grupos sean entre sí 
                lo más distintos posible.
                </p>
                <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <strong style="color: #4CAF50;">✅ Ventajas:</strong> Rápido y eficiente para grandes datasets
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.expander("🟢 IForest (Isolation Forest)", expanded=False):
            st.markdown("""
            <div style="background: rgba(76, 175, 80, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <p style="text-align: justify; line-height: 1.6;">
                El modelo IForest utiliza árboles de aislamiento para identificar puntos de datos anómalos. 
                Es eficiente y efectivo para detectar anomalías en grandes conjuntos de datos mediante el 
                principio de que las anomalías son más fáciles de aislar que los puntos normales.
                </p>
                <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <strong style="color: #4CAF50;">✅ Ventajas:</strong> Escalable y robusto contra outliers
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🔴 Autoencoder multiclase", expanded=False):
            st.markdown("""
            <div style="background: rgba(244, 67, 54, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <p style="text-align: justify; line-height: 1.6;">
                Este modelo combina un autoencoder tradicional con una capa de clasificación supervisada, 
                formando un único grafo computacional que optimiza simultáneamente la reconstrucción de 
                entrada y la predicción de su etiqueta.
                </p>
                <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <strong style="color: #4CAF50;">✅ Ventajas:</strong> Combina detección y clasificación
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Placeholder para imagen de modelos ML
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; 
                background: linear-gradient(45deg, #e8f5e8, #f1f8e9); 
                border-radius: 15px; border: 2px dashed #4caf50;">
        <h4 style="color: #2e7d32; margin-bottom: 1rem;">🤖 ESPACIO PARA VISUALIZACIÓN DE MODELOS</h4>
        <p style="color: #388e3c;">Diagramas explicativos de cada modelo de ML</p>
        <p style="color: #66bb6a; font-size: 0.9rem;">Dimensiones recomendadas: 800x600px</p>
    </div>
    """, unsafe_allow_html=True)

    # Guía de uso mejorada
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #E91E63; margin: 3rem 0 2rem 0;">
        📖 Guía de Uso del Sistema
    </h2>
    """, unsafe_allow_html=True)
    
    # Timeline de pasos
    steps = [
        {"icon": "🔌", "title": "Seleccionar Modelo", "desc": "Elige el algoritmo de detección más adecuado", "color": "#2196F3"},
        {"icon": "📡", "title": "Capturar Paquetes", "desc": "Inicia la captura de tráfico de red", "color": "#4CAF50"},
        {"icon": "🖱️", "title": "Realizar Predicción", "desc": "Ejecuta el análisis con un solo clic", "color": "#FF9800"},
        {"icon": "📊", "title": "Visualizar Resultados", "desc": "Examina gráficos interactivos y métricas", "color": "#9C27B0"},
        {"icon": "💾", "title": "Guardar Resultados", "desc": "Exporta los datos en formato CSV", "color": "#F44336"}
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1.5rem 0; 
                    background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px;
                    border-left: 4px solid {step['color']};">
            <div style="font-size: 3rem; margin-right: 2rem; min-width: 80px; text-align: center;">
                {step['icon']}
            </div>
            <div>
                <h4 style="color: {step['color']}; margin-bottom: 0.5rem;">
                    Paso {i}: {step['title']}
                </h4>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                    {step['desc']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Placeholder para screenshot del panel
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; 
                background: linear-gradient(45deg, #fafafa, #f5f5f5); 
                border-radius: 15px; border: 2px dashed #757575;">
        <h4 style="color: #424242; margin-bottom: 1rem;">🖥️ ESPACIO PARA CAPTURAS DEL PANEL</h4>
        <p style="color: #616161;">Screenshots del panel de control en funcionamiento</p>
        <p style="color: #9e9e9e; font-size: 0.9rem;">Dimensiones recomendadas: 1400x800px</p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de tipos de resultados mejorada
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #795548; margin: 3rem 0 2rem 0;">
        📊 Tipos de Resultados y Recomendaciones
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); 
                    padding: 2rem; border-radius: 15px; height: 465px; color: white;">
            <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">✅</div>
            <h4 style="text-align: center; margin-bottom: 1.5rem;">Resultados Normales</h4>
            <p style="text-align: justify; line-height: 1.6; margin-bottom: 1.5rem;">
                Los datos han sido clasificados como normales. No se han detectado anomalías significativas 
                en el tráfico de red analizado.
            </p>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
                <strong>💡 Recomendación:</strong><br>
                Continúa monitoreando la red regularmente para mantener la seguridad.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF9800 0%, #FFC107 100%); 
                    padding: 2rem; border-radius: 15px; height: 465px; color: white;">
            <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">⚠️</div>
            <h4 style="text-align: center; margin-bottom: 1.5rem;">Resultados Anómalos</h4>
            <p style="text-align: justify; line-height: 1.6; margin-bottom: 1.5rem;">
                Se han detectado patrones anómalos en la red. Esto puede indicar posibles amenazas 
                o comportamientos inusuales que requieren atención.
            </p>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
                <strong>🔍 Recomendación:</strong><br>
                Investiga las anomalías detectadas y toma medidas preventivas inmediatas.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F44336 0%, #E91E63 100%); 
                    padding: 2rem; border-radius: 15px; height: 465px; color: white; overflow-y: auto;">
            <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">🚨</div>
            <h4 style="text-align: center; margin-bottom: 1.5rem;">Ataques Específicos</h4>
            <!-- Tarjeta DDoS_TCP -->
            <div style="background:#ff5c5c;padding:1rem;border-radius:1rem;margin-bottom:1rem;color:white;">
                <strong>🔴 DDoS_TCP:</strong>
                <ul style="font-size: 0.9rem; margin-top: 0.5rem;">
                    <li>Activa SYN cookies</li>
                    <li>Configura límites de tasa</li>
                    <li>Usa ACL para bloquear IPs</li>
                </ul>
            </div>
            <!-- Tarjeta DDoS_UDP -->
            <div style="background:#ffb300;padding:1rem;border-radius:1rem;margin-bottom:1rem;color:white;">
                <strong>🟠 DDoS_UDP:</strong>
                <ul style="font-size: 0.9rem; margin-top: 0.5rem;">
                    <li>Permite solo puertos necesarios</li>
                    <li>Aplica límites de tasa UDP</li>
                    <li>Usa null routing</li>
                </ul>
            </div>
            <!-- Tarjeta Reconnaissance -->
            <div style="background:#2196f3;padding:1rem;border-radius:1rem;color:white;">
                <strong>🔵 Reconnaissance:</strong>
                <ul style="font-size: 0.9rem; margin-top: 0.5rem;">
                    <li>Restringe respuestas ICMP</li>
                    <li>Expón solo puertos necesarios</li>
                    <li>Configura límites anti-scan</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Placeholder final para imagen de dashboard
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 3rem; 
                background: linear-gradient(45deg, #e1f5fe, #f3e5f5); 
                border-radius: 15px; border: 2px dashed #673ab7;">
        <h4 style="color: #5e35b1; margin-bottom: 1rem;">📈 ESPACIO PARA DASHBOARD COMPLETO</h4>
        <p style="color: #7e57c2;">Vista general del dashboard con todas las métricas y gráficos</p>
        <p style="color: #9575cd; font-size: 0.9rem;">Dimensiones recomendadas: 1600x900px</p>
    </div>
    """, unsafe_allow_html=True)

    # Call-to-action mejorado
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #1E3D59 0%, #2E5077 100%); 
                padding: 3rem; border-radius: 20px; margin: 3rem 0;">
        <h3 style="color: white; margin-bottom: 1.5rem;">¿Listo para comenzar?</h3>
        <p style="color: #B8D4E3; font-size: 1.2rem; margin-bottom: 2rem;">
            Dirígete al Panel de Control para empezar a proteger tu red IoT
        </p>
        <div style="font-size: 2rem;">🚀</div>
    </div>
    """, unsafe_allow_html=True)

#---------------------------------------------------- DASHBOARD ----------------------------------------------------------------------------------------------------------------------------
# DistanceMetric.get_metric("euclidean") devuelve un objeto cuya clase interna
# es la que Python debe encontrar al desempaquetar el pickle.
_dm.EuclideanDistance = DistanceMetric.get_metric("euclidean").__class__



def show_dashboard_page():
    st.title('❇ Panel de Control de Detección')

    # Inicializa el flag una sola vez
    if 'prediccion_realizada' not in st.session_state:
        st.session_state['prediccion_realizada'] = False

    model_path = "model/lof_1_6_1_EJERCICIO10_n_components6_fit_over.pkl"
    loaded_object = joblib.load(model_path)
    print(f"Tipo del objeto cargado: {type(loaded_object)}")
    print(f"Contenido: {loaded_object}")
    
    model_path = "model/iforest__EJERCICIO10_n_components6_fit.pkl"
    loaded_object = joblib.load(model_path)
    print(f"Tipo del objeto cargado: {type(loaded_object)}")
    print(f"Contenido: {loaded_object}")
    
    model_path = "model/kmeans1_6_1__EJERCICIO10_n_components6_over.pkl"
    loaded_object = joblib.load(model_path)
    print(f"Tipo del objeto cargado: {type(loaded_object)}")
    print(f"Contenido: {loaded_object}")
    
    model_path = "model/dbscan_1_6_1_EJERCICIO10_n_components6_fit_over.pkl"
    loaded_object = joblib.load(model_path)
    print(f"Tipo del objeto cargado: {type(loaded_object)}")
    print(f"Contenido: {loaded_object}")
    
    model_path = "model/ocsvm__EJERCICIO10_n_components6_fit.pkl"
    loaded_object = joblib.load(model_path)
    print(f"Tipo del objeto cargado: {type(loaded_object)}")
    print(f"Contenido: {loaded_object}")
    
    
    
    # Rutas a los modelos
         
    LOF_MODEL_PATHS = "model/lof__EJERCICIO10_n_components6_fit_over.pkl"
    IFOREST_MODEL_PATHS = "model/iforest__EJERCICIO10_n_components6_fit.pkl"
    KMEANS_MODEL_PATHS = "model/kmeans1__EJERCICIO10_n_components6_over.pkl"
    DBSCAN_MODEL_PATHS= "model/dbscan__EJERCICIO10_n_components6_fit_over.pkl"
    DBSCAN_TXT_PATH="model/list_dbscan2_over.txt"
    KMEANS_TXT_PATH="model/list_kmeans_over.txt"
    AUTOENCODER_MODEL_PATH="model/autoencoder.pkl"
    OCSVM_MODEL_PATH="model/ocsvm__EJERCICIO10_n_components6_fit.pkl"


    def load_model(model_path):
        try:
            absolute_path = os.path.abspath(model_path)
            st.write(f"Intentando cargar desde: {absolute_path}")
            if not os.path.exists(absolute_path):
                raise FileNotFoundError(f"El archivo {absolute_path} no se encuentra.")
            model = joblib.load(absolute_path)
            st.write(f"Tipo del modelo cargado: {type(model)}")
            return model
        except Exception as e:
            st.error(f"Error al cargar el modelo: {str(e)}")
            import traceback
            st.error(f"Detalles del error: {traceback.format_exc()}")
            return None

    col1, col2 = st.columns([1, 2])

    # Columna derecha: bienvenida o resumen tras predicción
    with col2:
        if 'prediccion_realizada' not in st.session_state or not st.session_state['prediccion_realizada']:
            st.markdown("## 👋 Bienvenido al Panel IDS")
            st.info("Aquí verás el resumen y visualización de los resultados una vez realices una predicción.")
        else:
            st.markdown("## 📄 Resumen de la Predicción")
            resumen = st.session_state['resumen_prediccion']
            st.info(resumen['texto'])
            import plotly.express as px
            pie_fig = px.pie(
                names=resumen['labels'],
                values=resumen['values'],
                color=resumen['labels'],
                color_discrete_map={
                    'Normal': '#00C853',
                    'Anómalo': '#FF5252',
                    'DDOS_TCP': '#FF5252',
                    'DDOS_UDP': '#FFA726',
                    'Reconnaissance': '#42A5F5'
                },
                title="Distribución porcentual de clases"
            )
            pie_fig.update_traces(textinfo='percent+label')
            st.plotly_chart(pie_fig, use_container_width=True)
    
    # Interfas Uusuario Panel de Control
    with col1:
        st.markdown("### 🖥 Panel de Control")
        model_option = st.selectbox(
            "📌 Seleccione el modelo de detección",
            ('IForest','OCSVM','KMEANS','AUTOENCODER'),
            help="Cada modelo utiliza diferentes técnicas para detectar anomalías"
        )
        metric_option = st.selectbox(
            "📌 Seleccione el tipo de metrica",
            ('Externas', 'Internas'),
            help="Cada modelo utiliza diferentes técnicas para detectar anomalías"
        )
        
        
        # Función para procesar los paquetes capturados
        # ----------------------------------------------
        # Configuración del comando para Tshark
        comm_arg =  (
    "sudo /usr/local/bin/tshark "
    "-i eth0 -i wlan0 "
    "-l -c 1000 "
    "-Y 'eth.type != 0x8899' "
    # filtro de captura:
    "-f \"tcp or udp or arp\" "
    "-f \"arp or icmp or (udp and not port 53 and not port 5353) or (tcp and not port 443)\" "
    "-T fields -E separator=/t "
    "-e frame.time_delta "
    "-e _ws.col.Protocol "
    "-e ip.src -e ip.dst "
    "-e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 "
    "-e ipv6.src -e ipv6.dst "
    "-e eth.src -e eth.dst "
    "-e tcp.srcport -e tcp.dstport "
    "-e udp.srcport -e udp.dstport "
    "-e frame.len -e udp.length "
    "-e ip.ttl -e icmp.type "
    "-e ip.dsfield.dscp -e ip.flags.rb -e ip.flags.df -e ip.flags.mf "
    "-e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn "
    "-e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset "
    "-e tcp.flags.syn -e tcp.flags.fin -e ip.version "
    "-e frame.time_epoch"
)

        comm_arg = shlex.split(comm_arg)

        # Función para capturar paquetes
        def capturing_packets(comm_arg):
            process = Popen(comm_arg, stdout=PIPE, stderr=PIPE, text=True)
            return process

        # Función para transformar los paquetes en el formato correcto
        def type_packet(packet_):
            if len(packet_) < 34:  # Rellenar con valores vacíos si falta información
                packet_ += [''] * (34 - len(packet_))

            
            if packet_[1] == 'TCP' or packet_[1] == 'SSH' or packet_[1] == 'SSHv2' or packet_[1] == 'SSHv2' or packet_[1] == 'TLSv1.2' or packet_[1] == 'HTTP':
                tcp_src = packet_[10]  # campo tcp.srcport
                tcp_dst = packet_[11]  # campo tcp.dstport
            elif packet_[1] == 'UDP' or packet_[1]=='DNS' or packet_[1]=='BROWSER' or packet_[1]=='DHCP' :
                tcp_src = packet_[12]  # reasignación de udp.srcport a tcp.srcport
                tcp_dst = packet_[13]  # reasignación de udp.dstport a tcp.dstport
            else:
                tcp_src = ''
                tcp_dst = ''

                
            if packet_[1] == 'ARP':
                packet_[2] = packet_[4]  # ip.src <- arp.src.proto_ipv4
                packet_[3] = packet_[5]  # ip.dst <- arp.dst.proto_ipv4

            # Mapeo de IPv6 al campo IP src y dst
            if packet_[32] == '6':
                packet_[2] = packet_[6]  # ip.src <- ipv6.src
                packet_[3] = packet_[7]  # ip.dst <- ipv6.dst

 

            # Reemplazo de comas por puntos en ciertos campos
            for index in [16, 18, 19, 20, 21]:
                if packet_[index]:
                    packet_[index] = packet_[index].replace(',', '.')

            # Estructura del paquete ordenado
            #ordered_packet = [
                #packet_[0], packet_[1],tcp_src, tcp_dst, packet_[10], packet_[11], packet_[14],
                #packet_[15], packet_[16], packet_[17], packet_[18], packet_[19], packet_[20], packet_[21],
                #packet_[22], packet_[23], packet_[24], packet_[25], packet_[26], packet_[27], packet_[28],
                #packet_[29], packet_[30], packet_[31], packet_[32]
            #]

            ordered_packet = [
                packet_[0], packet_[1], packet_[2],packet_[3],tcp_src, tcp_dst,packet_[14], packet_[15],
                packet_[16], packet_[17], packet_[18], packet_[19], packet_[20], packet_[21], packet_[22],
                packet_[23], packet_[24], packet_[25], packet_[26], packet_[27], packet_[28], packet_[29],
                packet_[30], packet_[31], packet_[33]
            ]


            fieldnames = [
                'delta_time', 'protocols','ip_src','ip_dst','port_src', 'port_dst', 'frame_len',
                'udp_len', 'ip_ttl', 'icmp_type', 'tos', 'ip_flags_rb', 'ip_flags_df', 'ip_flags_mf',
                'tcp_flags_res', 'tcp_flags_ns', 'tcp_flags_cwr', 'tcp_flags_ecn', 'tcp_flags_urg',
                'tcp_flags_ack', 'tcp_flags_push', 'tcp_flags_reset', 'tcp_flags_syn', 'tcp_flags_fin','epoch_time'
            ]

            return {fieldnames[i]: [ordered_packet[i]] for i in range(len(fieldnames))}

        # Función para agregar los paquetes al DataFrame
        def packet_df(type_packet, df):
            df_temp = pd.DataFrame(type_packet)
            if list(df_temp.columns) == ['value']:
                return df  # Ignorar tablas value
            if df is None:
                df = df_temp
            else:
                df = pd.concat([df, df_temp], axis=0, ignore_index=True)
            # Si después de concatenar solo queda la columna value, devolver None
            if list(df.columns) == ['value']:
                return None
            return df
        
        def predecir(model, data, model_option):
            try:
                
                
                # Obtener las columnas desde el preprocesador
                columns = model[0].named_steps['prepro_2_del']\
                  .named_steps['prepro_1_num_cat']\
                  .get_feature_names_out().tolist()

                # Reemplazar del_columns en el pipeline con la versión correcta
                model[0].named_steps['prepro_2_del'].named_steps['del_columns'] = del_columns(columns)

              
                
                columnas=['number_delta_time',	'numbertcp_srcport',	'numbertcp_dstport',	'numberframe_len',	'numberudp_length',	'numberip_ttl',	'numbertos',	'numberip_flags_df',	'numberip_flags_mf',	'numbertcp_flags_ns',	'number_tcp_flags_syn','category__protocols'	]

                
                columnas_pca2=['componente1','componente2','componente3','componente4','componente5','componente6']

                #'category__protocols'
                if(model_option=='IForest'):
                    scores = model.decision_function(data)
                    predicciones=pred_threshold(scores, -0.10)
                    
                if(model_option=='LOF'):
                    scores = model.decision_function(data)
                    threshold = np.percentile(scores, 100 * 0.2)
                    st.write(threshold)
                    predicciones = np.where(scores >= threshold,0,1)

                if(model_option=='OCSVM'):
                    scores = model.decision_function(data)
                    threshold = np.percentile(scores, 100 * 0.45)
                    st.write(threshold)
                    predicciones = np.where(scores >= threshold,0,1)
                    #predicciones1=model.predict(data)
                    #predicciones=np.where(predicciones1 == 1, 0, 1)
                    #scores = model.decision_function(data)
                    #predicciones=pred_threshold(scores, 16000.512)
                if(model_option=='KMEANS'):
                    scores=""
                    predicciones=model.predict(data)
                    
                #if(model_option=='DBSCAN'):
                    #preproc = model.named_steps['preprocessor_3_pca']
                    #X = preproc.transform(data) # → pp3
                    #est = model.named_steps['dbscan']
                    #predicciones = est.fit_predict(X)
                    
                if model_option == 'DBSCAN':
                # 1) Transformación previa (PCA, escalado, etc.)
                    scores=""
                    preproc = model.named_steps['preprocessor_3_pca']
                    X = preproc.transform(data)  # → pp3

                    # 2) DBSCAN ya entrenado (lo cargaste con joblib)
                    db = model.named_steps['dbscan']

                    # 3) Asignación de etiquetas sin refit
                    predicciones = dbscan_predict(db, X)

                if(model_option=='AUTOENCODER'):
                    print("Aqui estan tus pesos: ", model.named_steps['autoencoder_classifier'].model.get_weights()[0].shape)
                    predicciones=model.predict(data)
                    scores=""
                    
                
                
                
                                
                pp3 = model[0].transform(data)  # Transformar los datos para el modelo IForest
                
                pp3 = pd.DataFrame(pp3, columns=columnas_pca2)  # Convertir a DataFrame
                
                # Añadir la columna de cluster al DataFrame
                pp3['cluster'] = predicciones
                
                
                return pp3, predicciones,scores
                
            except Exception as e:
                st.error(f"Error en la predicción: {str(e)}")
                import traceback
                st.error(f"Detalles: {traceback.format_exc()}")
                return None, None
        
        def mostrar_metricas(silhouette, calinski, davies):
          
           # Mostrar métricas en cards
            st.markdown("### 📊 Métricas Internas")
            cols = st.columns(3)
            with cols[0]:
                st.metric(
                    "Silhouette Score",
                    f"{silhouette:.3f}",
                    delta="Bueno" if silhouette > 0.5 else "Regular"
                )
            with cols[1]:
                st.metric(
                    "Calinski Score",
                    f"{calinski:.3f}",
                    delta="Bueno" if calinski > 1000 else "Regular"
                )
            with cols[2]:
                st.metric(
                    "Davies Score",
                    f"{davies:.3f}",
                    delta="Bueno" if davies < 0.5 else "Regular"
                )     
                            
                     

        # Función para guardar los paquetes en CSV
        def save_packet_csv(df, path):
            df.to_csv(path, index=False)
            st.success(f"✅ Archivo guardado en {path}")
            
        # Streamlit UI
        st.title("🔍 Captura y Análisis de Tráfico de Red")

        traffic_method = st.selectbox(
            "📌 Seleccione el método de tráfico",
            ('Iniciar captura de paquetes', 'Abrir captura de paquetes pcap')
        )

        data = None  # Inicializamos el DataFrame

        if traffic_method == 'Iniciar captura de paquetes':

            if st.button("🚀 Iniciar Captura"):
                process = capturing_packets(comm_arg)
                st.write("📡 Capturando paquetes...")

                # Inicializamos el DataFrame
                captured_data = None
                progress_bar = st.progress(0, text="Capturando paquetes...")
                total_packets = 100

                for i in range(total_packets):  # Capturar 100 paquetes
                    packet_str = process.stdout.readline().strip()
                    if packet_str:
                        packet_list = packet_str.split("\t")  # Separar los datos por tabulación
                        type_packet_data = type_packet(packet_list)  # Convertir a estructura correcta
                        captured_data = packet_df(type_packet_data, captured_data)  # Agregar al DataFrame
                    progress_bar.progress((i + 1) / total_packets, text=f"Paquetes capturados: {i+1}/{total_packets}")

                process.terminate()
                progress_bar.empty()
                st.success("✅ Captura finalizada.")

                # Mostrar el DataFrame capturado
                if captured_data is not None and list(captured_data.columns) != ['value']:
                    st.write("📊 *Paquetes capturados:*")
                    st.dataframe(captured_data)
                    st.session_state.data = captured_data
                    st.success("Datos capturados listos para predicción")
                    
                    # Guardar los datos capturados en la sesión
                    st.session_state.data = captured_data
                    
                    # Mostrar mensaje de confirmación
                    st.success("Datos capturados listos para predicción")
                    
                    # Botón para guardar en CSV (opcional)
                    if st.button("💾 Guardar en CSV"):
                        save_packet_csv(captured_data, "captura_paquetes.csv")

        # Sección de carga de archivo CSV
        with st.container():
            st.markdown("### 📊 Cargar Datos para Predicción")
            
            # Si hay datos capturados, mostrar mensaje
            if 'data' in st.session_state and st.session_state.data is not None:
                st.info("✅ Usando datos de la captura de paquetes")
                data = st.session_state.data
                st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos capturados listos para predicción</div>', unsafe_allow_html=True)
            else:
                # De lo contrario, mostrar el cargador de archivo CSV
                uploaded_file = st.file_uploader(
                    "📂 Cargar archivo CSV",
                    type="csv",
                    help="Cargue sus datos de red en formato CSV",
                    key="csv_uploader_1"
                )
                
                if uploaded_file is not None:
                    data = pd.read_csv(uploaded_file)
                    st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos cargados exitosamente</div>', unsafe_allow_html=True)
                    
                    with st.expander("📊 Vista previa de datos"):
                        st.dataframe(data.head())
                        st.info(f"Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")
                else:
                    data = None

        if st.button('🚀 Realizar Predicción', key='predict'):
                
            if data is not None:
                loading_placeholder = st.empty()
                #with loading_placeholder.container():
                    #if lottie_loading is not None:
                        #st_lottie(lottie_loading, height=200, key="loading")
                
                try:
                    # Inicializar el modelo
                    model = None
                    
                    # Cargar el modelo según la opción seleccionada
                    if model_option == 'IForest':
                        model = load_model(IFOREST_MODEL_PATHS)
                    elif model_option=='LOF':
                        model=load_model(LOF_MODEL_PATHS)
                    elif model_option=='OCSVM':
                        model=load_model(OCSVM_MODEL_PATH)
                    elif model_option=='KMEANS':
                        model = load_model(KMEANS_MODEL_PATHS)
                    elif model_option=='DBSCAN':
                        model=load_model(DBSCAN_MODEL_PATHS)
                    elif model_option=='AUTOENCODER':
                        model=load_model(AUTOENCODER_MODEL_PATH)
                        if model is None:
                            raise Exception("No se pudo cargar el modelo IForest")
                    if model is None:
                        raise Exception("No se pudo cargar el modelo seleccionado")
                
                    
                    if traffic_method == 'Iniciar captura de paquetes':
                                  
                        lista=['ip_ttl',  'tos','ip_flags_rb','ip_flags_df','ip_flags_mf']
                        #tipo string, para reemplazar un coma por el punto y convertirlo en float
                        data[lista] = data[lista].astype('str')
                        data.ip_ttl = data.ip_ttl.str.replace(',','.')
                        data.tos = data.tos.str.replace(',','.')
                        data.ip_flags_rb = data.ip_flags_rb.str.replace(',','.')
                        data.ip_flags_df = data.ip_flags_df.str.replace(',','.')
                        data.ip_flags_mf = data.ip_flags_mf.str.replace(',','.')
                    #   data[lista] = data[lista].astype('float64')
                        
                        data = data.replace('', np.nan).fillna(0)
                        # Realizar predicción
                        start_time = time.time()
                        psutil.cpu_times()
                        psutil.virtual_memory()
                        psutil.disk_partitions()

                        t_cpu = psutil.cpu_times()
                        start_user = t_cpu.user
                        cpu_usage = psutil.cpu_percent(1)
                        mem_usage = psutil.virtual_memory().percent
                        disco2 = psutil.disk_usage('/')
                        pp3, y_pred,scores = predecir(model, data, model_option)

                        #st.session_state.y_pred = y_pred
                        
                        if(model_option=='KMEANS' or model_option=='DBSCAN'):
                            
                            if(model_option=='KMEANS'):
                                path2=KMEANS_TXT_PATH
                            else:
                                path2=DBSCAN_TXT_PATH
                                
                            dict_pred=dict_predict(path2)
                            #etiqueta=dict_pred[cluster[-1]]
                            etiquetas = [ dict_pred[c] for c in y_pred ]

                            y_pred_etiqueta=etiquetas

                                    
                            # 2) Cuenta cada etiqueta
                            conteo = Counter(etiquetas)

                            # 3) Guarda en un diccionario todas las cuentas
                            label_counts = dict(conteo)
                            normal_count         = label_counts.get('Normal', 0)
                            ddos_tcp_count       = label_counts.get('DDoS_TCP', 0)
                            ddos_udp_count       = label_counts.get('DDoS_UDP', 0)
                            reconnaissance_count = label_counts.get('Reconnaissance', 0)

                            

                        elif(model_option=='AUTOENCODER'):
                            # Supongamos que tus etiquetas predichas están en YA_pred
                            normal_count = np.count_nonzero(y_pred == 0)
                            ddos_tcp_count = np.count_nonzero(y_pred == 1)
                            reconnaissance_count = np.count_nonzero(y_pred == 2)
                            ddos_udp_count = np.count_nonzero(y_pred == 3)

                            

                            # Condiciones y etiquetas
                            condiciones = [
                                y_pred == 0,
                                y_pred == 1,
                                y_pred == 2,
                                y_pred == 3
                            ]
                            etiquetas = [
                                'Normal',
                                'DDoS_TCP',
                                'Reconnaissance',
                                'DDoS_UDP'
                            ]

                            # Reemplazo
                            y_pred_etiqueta = np.select(condiciones, etiquetas, default='Desconocido')

                        else:
                            n_normales  = int((y_pred == 0).sum())
                            n_anomalos  = int((y_pred == 1).sum())

                            # Condiciones y etiquetas
                            condiciones = [
                                y_pred == 0,
                                y_pred == 1,
                            ]
                            etiquetas = [
                                'Normal',
                                'Ataque'
                            ]

                            # Reemplazo
                            y_pred_etiqueta = np.select(condiciones, etiquetas, default='Desconocido')

                        
                            st.write(n_normales,n_anomalos)
                            # No imprimir 'scores' para evitar tabla 'value'

                        st.session_state.y_pred_etiqueta = y_pred_etiqueta

                        # Guardar resumen para mostrar en col2
                        st.session_state['prediccion_realizada'] = True
                        if model_option in ['KMEANS', 'DBSCAN', 'AUTOENCODER']:
                            total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                            texto = f"Se analizaron {total} paquetes. El sistema clasificó {normal_count} como Normal, {ddos_tcp_count} como DDOS_TCP, {ddos_udp_count} como DDOS_UDP y {reconnaissance_count} como Reconnaissance."
                            labels = ['Normal', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance']
                            values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                        else:
                            total = n_normales + n_anomalos
                            texto = f"Se analizaron {total} paquetes. El sistema clasificó {n_normales} como normales y {n_anomalos} como anómalos."
                            labels = ['Normal', 'Anómalo']
                            values = [n_normales, n_anomalos]
                        st.session_state['resumen_prediccion'] = {'texto': texto, 'labels': labels, 'values': values}

                        # Forzar refresco para que col2 cambie de "Bienvenido" a "Resumen" inmediatamente
                        try:
                            st.rerun()
                        except Exception:
                            st.experimental_rerun()
                            
                        if pp3 is None or y_pred is None:
                            raise Exception("Error en la predicción")
                    
                    # --- Parte métricas internas ---
                    # Para cualquier algoritmo necesitamos al menos 2 clusters distintos
                    unique_labels = np.unique(y_pred)
                    if len(unique_labels) >= 2:
                        silhouette, calinski, davies = metricas.metrica_internas(pp3, y_pred)
                        if metric_option == 'Internas':
                            mostrar_metricas(silhouette, calinski, davies)
                    else:
                        st.write("No se pueden calcular las métricas porque sólo hay un clúster")
                    
                    
                    # Limpiar animación de carga
                    time.sleep(3)
                    loading_placeholder.empty()
                    
                    # Sección de visualización
                    # Sección de visualización
                    with col1:
                        # Contar normales y anómalos usando y_pred
                        if(model_option=='IForest' or model_option=='LOF' or model_option=='OCSVM'):
                            st.write(f"Normales: {n_normales}, Anómalos: {n_anomalos}")

                            # Crear gráfico de barras con Plotly
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=['Normal', 'Anómalo'],
                                    y=[n_normales, n_anomalos],
                                    marker_color=['#00C853', '#FF5252'],
                                    text=[f"{n_normales:,}", f"{n_anomalos:,}"],
                                    textposition='auto',
                                    hoverinfo='y+text',
                                    width=0.8
                                )
                            ])
                            fig.update_layout(
                                title="Distribución de Detecciones",
                                title_x=0.5,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'),
                                showlegend=False,
                                margin=dict(t=50, l=50, r=50, b=50),
                                width=800,
                                height=700,
                                xaxis=dict(
                                    title="Clasificación",
                                    showgrid=False,
                                    showline=True,
                                    linecolor='rgba(255,255,255,0.2)'
                                ),
                                yaxis=dict(
                                    title="Cantidad",
                                    showgrid=True,
                                    gridcolor='rgba(255,255,255,0.1)',
                                    zeroline=False
                                ),
                                bargap=0.2
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                        elif(model_option=='KMEANS' or model_option=='DBSCAN' or model_option=='AUTOENCODER'):
                            st.write(f"Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP:{ddos_udp_count}, Reconnaisance:{reconnaissance_count}")

                            # Crear gráfico de barras con Plotly
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=['Normal', 'DDOS_TCP','DDOS_UDP','Reconnaisance'],
                                    y=[normal_count, ddos_tcp_count,ddos_udp_count,reconnaissance_count],
                                    marker_color=['#00C853', '#FF5252', '#FF5252', '#FF5252'],
                                    text=[f"{normal_count:,}", f"{ddos_tcp_count:,}", f"{ddos_udp_count:,}", f"{reconnaissance_count:,}"],
                                    textposition='auto',
                                    hoverinfo='y+text',
                                    width=0.8
                                )
                            ])
                            fig.update_layout(
                                title="Distribución de Detecciones",
                                title_x=0.5,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'),
                                showlegend=False,
                                margin=dict(t=50, l=50, r=50, b=50),
                                width=950,
                                height=700,
                                xaxis=dict(
                                    title="Clasificación",
                                    showgrid=False,
                                    showline=True,
                                    linecolor='rgba(255,255,255,0.2)'
                                ),
                                yaxis=dict(
                                    title="Cantidad",
                                    showgrid=True,
                                    gridcolor='rgba(255,255,255,0.1)',
                                    zeroline=False
                                ),
                                bargap=0.2
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                        st.markdown("### 💻 Rendimiento de Recursos")
                        tiempo_total = time.time() - start_time
                        cols = st.columns([2, 1])
                        with cols[0]:
                            met_cols = st.columns(4)
                            with met_cols[0]:
                                st.metric("⏱️ Tiempo (s)", f"{tiempo_total:.2f}")
                            with met_cols[1]:
                                st.metric("🖥️ % CPU", f"{cpu_usage:.2f}%")
                            with met_cols[2]:
                                st.metric("💾 % Memoria", f"{mem_usage:.2f}%")
                            with met_cols[3]:
                                st.metric("📀 % Disco", f"{disco2[3]:.2f}%")
                        # El resumen y la gráfica se muestran únicamente en la columna derecha (col2)
                

                except Exception as e:
                    st.error(f"❌ Error en el procesamiento: {str(e)}")
                    import traceback
                    st.error(f"Detalles: {traceback.format_exc()}")
                    loading_placeholder.empty()
            else:
                st.warning("⚠ Por favor capture paquetes o cargue un archivo CSV antes de realizar la predicción.")

        
        
        LABEL = "Ingresa el nombre para tu archivo" 
        
        # 2. Abrimos el div contenedor
        st.markdown('<div class="mi-caja">', unsafe_allow_html=True)

        # 3. Este text_input (label + input) queda dentro de .mi-caja
        nombre_archivo = st.text_input(LABEL)

        # 4. Cerramos el div
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Guardar csv"):
            data = st.session_state.data
            y_pred = st.session_state.y_pred_etiqueta

            # Si y_pred es una lista o array, conviértelo en DataFrame para concatenar
            if not isinstance(y_pred, pd.DataFrame):
                y_pred = pd.DataFrame(y_pred, columns=["predicción"])

            resultado = pd.concat([data.reset_index(drop=True), y_pred.reset_index(drop=True)], axis=1)
            resultado.to_csv(nombre_archivo+'.csv', index=False)
            st.success("✅ CSV guardado correctamente.")
        else:
            st.warning("⚠ Primero debes capturar tráfico o hacer una predicción antes de guardar.") 
        
    

    with col2:
        if uploaded_file is not None:
            with st.spinner('⏳ Procesando datos...'):
                data = pd.read_csv(uploaded_file)
                st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos cargados exitosamente</div>', unsafe_allow_html=True)
                time.sleep(3)

                with st.expander("📊 Vista previa de datos"):
                    st.dataframe(data.head())
                    st.info(f"Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")

    if uploaded_file is not None and st.button('🚀 Realizar Predicción', key='predict'):
        loading_placeholder = st.empty()
        cancel_button = st.empty()
        with loading_placeholder.container():
            #if lottie_loading is not None:
                #st_lottie(lottie_loading, height=200, key="loading")
                #cancel_button.button("Cancelar Predicción", key='cancel')
        
        
            if model_option == 'IForest':
                # Cargar directamente el modelo OCSVM
                model = load_model(IFOREST_MODEL_PATHS)
                current_models = None  # No necesitamos current_models aquí
            else:
                # Seleccionar rutas para los otros modelos
                if model_option == 'LOF':
                    MODEL_PATHS = LOF_MODEL_PATHS
                elif model_option == 'IForest':
                    MODEL_PATHS = IFOREST_MODEL_PATHS
                elif model_option == 'KNN':
                    MODEL_PATHS = KNN_MODEL_PATHS
            # Cargar modelos desde las rutas
                current_models = load_models(MODEL_PATHS)
               
            # Procesamiento de datos para otros modelos
             
        #    for i, (key, model) in enumerate(current_models.items()):  
                
                if traffic_method == 'Iniciar captura de paquetes':
                
                    pp3,y_pred=predecir(model,captured_data) 
                    
                    silhouette,calinski,davies = metricas.metrica_internas(pp3,pp3['cluster'])  
                    
                    mostrar_metricas(silhouette,calinski,davies)   
                
                    
            # Limpiar animación de carga después de 3 segundos
            time.sleep(3)
            loading_placeholder.empty()
    
    
            
                
            # Mostrar animación de éxito
            with st.container():
                if lottie_success:
                    st_lottie(lottie_success, height=200, key="success", speed=1.5)
                    time.sleep(3)

            # Resultados y visualizaciones
             # Visualization section
            # Sección de visualización
            col1, col2 = st.columns(2)
            

        with col1:
            
            num_clusters = len(np.unique(pp3['cluster']))
                            # Cálculo de las cantidades de normales y anómalos

            if num_clusters >  1:
                normal_count = np.sum(pp3['cluster'] == 1)
                anomaly_count = np.sum(pp3['cluster'] == -1)
            else:
                normal_count = np.sum(pp3['cluster'] == 1)
                anomaly_count = 0
            st.write(normal_count, anomaly_count)    

            # Crear el gráfico de barras con Plotly
            fig = go.Figure(data=[
                go.Bar(
                    x=['Normal', 'Anómalo'],  # Etiquetas del eje X
                    y=[normal_count, anomaly_count],  # Valores del eje Y
                    marker_color=['#00C853', '#FF5252'],  # Colores personalizados
                    text=[f"{normal_count:,}", f"{anomaly_count:,}"],  # Texto en las barras
                    textposition='auto',  # Posición del texto
                    hoverinfo='y+text',  # Información al pasar el mouse
                    width=0.8  # Ancho de las barras
                )
            ])

            # Configuración de diseño del gráfico
            fig.update_layout(
                title="Distribución de Detecciones",  # Título del gráfico
                title_x=0.5,  # Centrar el título
                plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del área de trazado
                paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del gráfico
                font=dict(color='white'),  # Color del texto
                showlegend=False,  # Ocultar leyenda
                margin=dict(t=50, l=50, r=50, b=50),  # Márgenes del gráfico
                width=800,  # Ancho total del gráfico
                height=700,  # Altura total del gráfico
                xaxis=dict(
                    title="Clasificación",
                    showgrid=False,
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    title="Cantidad",
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    zeroline=False
                ),
                bargap=0.2
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig, use_container_width=True) 
                
                
            
            # Matriz de Confusión
            
            def confusion_matrix_threshold(actual,score, threshold):
                Actual_pred = pd.DataFrame({'Actual': actual, 'Pred': score})
                Actual_pred['Pred'] = np.where(Actual_pred['Pred']<=threshold,0,1)
                cm = pd.crosstab(Actual_pred['Actual'],Actual_pred['Pred'])
                return(cm)
            
            if(metric_option=='Externas'):
                with st.expander("📖 Explicación de las métricas Externas"):
                        
                        st.write("""
                        1. Precisión (Precision):
                        - Indica qué porcentaje de las predicciones positivas realizadas por el modelo son correctas.
                        - Fórmula: TP / (TP + FP)
                        - Ejemplo: Si el modelo predice 100 positivos y 98 son correctos, la precisión es 0.98.

                        2. Exactitud (Accuracy):
                        - Porcentaje de predicciones correctas sobre el total de predicciones realizadas.
                        - Fórmula: (TP + TN) / (TP + TN + FP + FN)
                        - Muestra qué tan bien el modelo clasifica en general.

                        3. F1-Score:
                        - Es la media armónica entre la Precisión y la Sensibilidad (Recall).
                        - Útil cuando las clases están desbalanceadas.
                        - Fórmula: 2 * (Precision * Recall) / (Precision + Recall)

                        4. Curva ROC y AUC:
                        - La curva ROC muestra la relación entre la Tasa de Verdaderos Positivos (TPR) y la Tasa de Falsos Positivos (FPR).
                        - El AUC (Área Bajo la Curva) mide qué tan bien el modelo separa las clases.
                        - Un valor cercano a 1 indica un excelente desempeño; 0.76 es aceptable.

                        5. Falsos Positivos (FP):
                        - Representan los casos negativos que el modelo clasificó erróneamente como positivos.
                        - Fórmula: FP / (FP + TN)
                        - Menos falsos positivos indican mejor rendimiento.

                        6. Falsos Negativos (FN):
                        - Representan los casos positivos reales que el modelo no detectó correctamente.
                        - Fórmula: FN / (FN + TP)
                        - Un valor bajo indica que el modelo es bueno para detectar positivos reales.

                        Nota:
                        - TP: Verdaderos Positivos
                        - TN: Verdaderos Negativos
                        - FP: Falsos Positivos
                        - FN: Falsos Negativos
                        """)    
                st.markdown("### 📊 Matriz de Confusión")
                data_y=datay.values
                matrix_confusion = confusion_matrix_threshold(datay, average_scores, threshold)
                st.table(matrix_confusion.style.format("{:,.0f}"))
                # Explicación interactiva
                with st.expander("📖 ¿Qué es la Matriz de Confusión?"):
                    st.markdown("""
                        La Matriz de Confusión es una herramienta para evaluar el desempeño de un modelo de clasificación. 
                        Muestra la cantidad de predicciones correctas e incorrectas de un modelo en una tabla con cuatro categorías:
                        - Verdaderos positivos (TP): Predicciones correctas de la clase positiva.
                        - Falsos negativos (FN): Predicciones incorrectas donde el modelo predijo la clase negativa.
                        - Verdaderos negativos (TN): Predicciones correctas de la clase negativa.
                        - Falsos positivos (FP): Predicciones incorrectas donde el modelo predijo la clase positiva.
                    """)
                
            if(metric_option=='Internas'):
                with st.expander("📖 Explicación de las métricas Internas"):
                        
                        st.write("""
                        1. Silhouette Score:
                        - El puntaje de silueta es una medida utilizada para evaluar la calidad de un agrupamiento (clustering) en un conjunto de datos.
                        - Se basa en la distancia entre los puntos de datos y su relación con otros grupos.
                        - Un valor cercano a 1 indica que el punto está bien agrupado.
                        - Un valor cercano a 0 indica que el punto está en la frontera entre dos grupos.
                        - Un valor negativo indica que el punto podría estar mal agrupado.

                        2. Calinski-Harabsz Score:
                        - Mide la relación entre la suma de las distancias dentro de los clusters y la suma de las distancias entre clusters.
                        - Un valor más alto indica clusters más separados y bien definidos.

                        3. Davies-bouldin Score:
                        - Se enfoca en la similitud entre pares de clusters, considerando tanto la compacidad como la separación.
                        - Cuanto más bajo sea el índice, más separados y compactos serán los clusters, lo que indica un agrupamiento de mayor calidad.
                        

                        """)    
            
            # New Traffic Pattern Visualization
            st.markdown("### 📈 Patrón de Tráfico y Anomalías")
            
            # Calculate traffic metrics
            traffic_data = data.mean(axis=1)  # Using mean of all features as traffic indicator
            
            # Calculate ceiling and floor
            window = 20  # Window size for rolling calculations
            ceiling = traffic_data.rolling(window=window).max()
            floor = traffic_data.rolling(window=window).min()
            
            # Create traffic pattern figure
            fig_traffic = go.Figure()

            # Add main traffic line
            fig_traffic.add_trace(go.Scatter(
                x=list(range(len(traffic_data))),
                y=traffic_data,
                mode='lines',
                name='Tráfico',
                line=dict(color='#4B9FE1', width=1)
            ))

            # Add ceiling line
            fig_traffic.add_trace(go.Scatter(
                x=list(range(len(ceiling))),
                y=ceiling,
                mode='lines',
                name='Techo',
                line=dict(color='#00C853', width=2, dash='dash')
            ))

            # Add floor line
            fig_traffic.add_trace(go.Scatter(
                x=list(range(len(floor))),
                y=floor,
                mode='lines',
                name='Suelo',
                line=dict(color='#FFA726', width=2, dash='dash')
            ))

            # Add anomaly points
            anomaly_indices = np.where(y_pred == 1)[0]
            fig_traffic.add_trace(go.Scatter(
                x=anomaly_indices,
                y=traffic_data[anomaly_indices],
                mode='markers',
                name='Anomalías',
                marker=dict(
                    color='#FF5252',
                    size=8,
                    symbol='circle'
                )
            ))

            # Update layout
            fig_traffic.update_layout(
                title="Patrón de Tráfico y Detección de Anomalías",
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(t=50, l=50, r=50, b=50),
                xaxis=dict(
                    title="Muestras",
                    showgrid=False,
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    title="Intensidad de Tráfico",
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    zeroline=False
                )
            )

            st.plotly_chart(fig_traffic, use_container_width=True)
                
            with col2:
                
                # Métricas de rendimiento
                X_test_norm = data.values
                if metric_option== 'Externas':
                    data_y=datay.values
                    #Matriz de confusion
                    def confusion_matrix_threshold(actual,score, threshold):
                        Actual_pred = pd.DataFrame({'Actual': actual, 'Pred': score})
                        Actual_pred['Pred'] = np.where(Actual_pred['Pred']<=threshold,0,1)
                        cm = pd.crosstab(Actual_pred['Actual'],Actual_pred['Pred'])
                        return(cm)
                    matrix_confusion=confusion_matrix_threshold(datay,average_scores,threshold)
                    
                    
                    #Metricas supervisadas
                    def Metricas_precision(Matriz):
                        # Cálculo de precisión
                        Precision = Matriz.iloc[0,0] / (Matriz.iloc[0,0] + Matriz.iloc[0,1])
                        
                        # Cálculo de exactitud
                        Exactitud = (Matriz.iloc[0,0] + Matriz.iloc[1,1]) / (Matriz.iloc[0,0] + Matriz.iloc[0,1] + Matriz.iloc[1,0] + Matriz.iloc[1,1])
                        
                        # Cálculo de especificidad
                        Especificidad = Matriz.iloc[1,1] / (Matriz.iloc[1,1] + Matriz.iloc[0,1])
                        
                        # Cálculo de la tasa de verdaderos positivos (TVP o Sensibilidad)
                        TVP = Matriz.iloc[0,0] / (Matriz.iloc[0,0] + Matriz.iloc[1,0])
                        
                        # Tasa de falsos negativos (TasaFN o FNR)
                        TasaFN = Matriz.iloc[1,0] / (Matriz.iloc[1,0] + Matriz.iloc[0,0])
                        
                        # Tasa de falsos positivos (TasaFP o FPR)
                        TasaFP = Matriz.iloc[0,1] / (Matriz.iloc[0,1] + Matriz.iloc[1,1])
                        
                        # Valor predictivo positivo (VPP o Precisión)
                        VPP = Matriz.iloc[0,0] / (Matriz.iloc[0,1] + Matriz.iloc[0,0])
                        
                        # Valor predictivo negativo (VPN)
                        VPN = Matriz.iloc[1,1] / (Matriz.iloc[1,1] + Matriz.iloc[1,0])
                        
                        # Cálculo de F1 Score
                        F1 = (2 * Precision * TVP) / (Precision + TVP)
                        return Precision, Exactitud, Especificidad, TVP, TasaFN, TasaFP, VPP, VPN, F1

                    Precision_n, Exactitud_n, Especificidad_n, TVP_n, TasaFN_n, TasaFP_n, VPP_n, VPN_n, F1_n=Metricas_precision(matrix_confusion)
                      
                    
                    Actual_predIF = pd.DataFrame({'Actual': datay, 'Pred':average_scores})
                    Actual_predIF['Pred'] = np.where(Actual_predIF['Pred']<=threshold,0,1)
                    actual=Actual_predIF['Actual']
                    pred=Actual_predIF['Pred']
                    
                    
                    with col2:
                        
                        
                    # Curva ROC
                        def plot_roc_curve(true_y, y_prob):
                            fpr, tpr, thresholds = roc_curve(true_y, y_prob)
                            roc_auc = auc(fpr, tpr)

                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=fpr,
                                y=tpr,
                                mode='lines',
                                name=f'ROC curve = {roc_auc:.2f}',
                                line=dict(color='red', width=2)
                            ))
                            fig.add_trace(go.Scatter(
                                x=[0, 1],
                                y=[0, 1],
                                mode='lines',
                                name='Random Guess',
                                line=dict(color='blue', dash='dash', width=2)
                            ))

                            fig.update_layout(
                                title="Curva ROC",
                                title_x=0.5,
                                xaxis=dict(
                                    title="Tasa de Falsos Positivos (FPR)",
                                    range=[0, 1],
                                    gridcolor='rgba(255,255,255,0.1)',
                                    linecolor='rgba(255,255,255,0.2)',
                                    tickcolor='rgba(255,255,255,0.5)',
                                    showgrid=True,
                                    zeroline=False
                                ),
                                yaxis=dict(
                                    title="Tasa de Verdaderos Positivos (TPR)",
                                    range=[0, 1],
                                    gridcolor='rgba(255,255,255,0.1)',
                                    linecolor='rgba(255,255,255,0.2)',
                                    tickcolor='rgba(255,255,255,0.5)',
                                    showgrid=True,
                                    zeroline=False
                                ),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white', size=12),
                                legend=dict(
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    bgcolor="rgba(0,0,0,0)"
                                )
                            )

                            st.plotly_chart(fig, use_container_width=True)

                        plot_roc_curve(actual, pred)
                        curve_roc = roc_auc_score(actual, pred)
                    
                    
                    # Explicación interactiva para la curva ROC
                    with st.expander("📖 ¿Qué es la Curva ROC?"):
                        
                    
                        st.markdown("""
                    La Curva ROC (Receiver Operating Characteristic) muestra la relación entre la tasa de verdaderos positivos 
                    (TPR) y la tasa de falsos positivos (FPR) en diferentes umbrales de clasificación. 
                    - AUC (Área bajo la curva): Indica la capacidad del modelo para distinguir entre las clases.
                    - Cuanto mayor sea el área bajo la curva (AUC), mejor será el rendimiento del model""")        
                        
                    # Mostrar métricas en cards
                    st.markdown("### 📊 Métricas Externas")
                    cols = st.columns(6)
                    with cols[0]:
                        st.metric(
                            "Precision",
                            f"{Precision_n:.2f}",
                            delta="Bueno" if Precision_n > 0.75 else "Regular"
                        )
                    with cols[1]:
                        st.metric(
                            "Exactitud",
                            f"{Exactitud_n:.1f}",
                            delta="Bueno" if Exactitud_n > 0.75 else "Regular"
                        )
                    with cols[2]:
                        st.metric(
                            "F1-SCORES",
                            f"{F1_n:.2f}",
                            delta="Bueno" if F1_n > 0.75 else "Regular"
                        )
                    with cols[3]:
                        st.metric(
                            "Curve ROC",
                            f"{curve_roc:.2f}",
                            delta="Bueno" if curve_roc > 0.75 else "Regular"
                        )
                    with cols[4]:
                        st.metric(
                            "Falsos positivos",
                            f"{TasaFP_n:.2f}",
                            delta="Bueno" if TasaFP_n < 0.3 else "Regular"
                        )
                    with cols[5]:
                        st.metric(
                            "Falsos Negativos",
                            f"{TasaFN_n:.2f}",
                            delta="Bueno" if TasaFN_n < 0.3 else "Regular"
                        )
                    
                
                        
            # Tabla de resultados detallados
            with st.expander("📑 Detalles de las Predicciones"):
                results_df = pd.DataFrame({
                    'ID': data.index,
                    'Score de Anomalía': average_scores,
                    'Clasificación': ['0' if x == 0 else '1' for x in y_pred]
                })
                st.dataframe(results_df, use_container_width=True)


# Control de navegación
if st.session_state.page == "home":
    show_home_page()
else:
    show_dashboard_page()

# Pie de página mejorado
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🛡 Sistema de Detección de Anomalías IoT</p>
            <p>© 2024 Innovasic | UCC</p>
        </div>
        """,
        unsafe_allow_html=True)
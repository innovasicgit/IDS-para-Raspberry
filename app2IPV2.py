import streamlit as st
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
import sklearn
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
from sklearn.base import BaseEstimator, ClassifierMixin
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
import time
from autoencoder_classifier import AutoencoderClassifier

from frontend.style import setup_page_and_style
from frontend.home_page import show_home_page
from frontend.auth_ui import ensure_auth
from frontend.pdf_report import generar_reporte_pdf, DESCRIPCIONES_AMENAZAS
from backend.constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH,
)
from backend.model_utils import load_model, dict_predict, pred_threshold, dbscan_predict
from backend.capture_utils import (
    build_tshark_command,
    capturing_packets,
    type_packet,
    packet_df,
)
from backend.arp_filter import apply_realtime_arp_filter, get_arp_filter_description
from backend.notifications import NotificationManager
from backend.notifications_db import NotificationsDB
from backend.predict import predecir, mostrar_metricas

# Configuración de página y estilos (primera llamada a Streamlit)
setup_page_and_style()

# (Estilos y configuración aplicados por setup_page_and_style)
ensure_auth()

# Inicializar NotificationManager en session_state si no existe
if 'notification_manager' not in st.session_state:
    st.session_state.notification_manager = NotificationManager()

# Inicializar NotificationsDB para persistencia
if 'notifications_db' not in st.session_state:
    st.session_state.notifications_db = NotificationsDB()
    
    # Cargar configuración guardada
    db = st.session_state.notifications_db
    saved_config = db.load_email_config()
    saved_enabled = db.load_preferences()
    
    # Cargar en session_state
    st.session_state.user_email = saved_config.get('recipient_email', '')
    st.session_state.gmail_user = saved_config.get('gmail_user', '')
    st.session_state.gmail_app_password = saved_config.get('gmail_app_password', '')
    st.session_state.enable_email_notifications = saved_enabled

# Autenticación via módulo externo


# ---------------------------------------------------- INICIO PAGE----------------------------------------------------------------------------------------------------------------------------
# Navegación mejorada
from pathlib import Path

with st.sidebar:
    logo_path = Path(__file__).parent / "img" / "logo.png"
    st.image(str(logo_path), width=150)
    if st.session_state.get("authenticated"):
        st.caption(f"Conectado como: {st.session_state.username}")
        if st.button("Cerrar sesión", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    selected = option_menu(
        "Navegación",
        ["Inicio", "Panel de Control", "Comparar Modelos"],
        icons=["house", "graph-up", "bar-chart"],
        menu_icon="cast",
        default_index=0
    )

    if selected == "Inicio":
        st.session_state.page = "home"
    elif selected == "Panel de Control":
        st.session_state.page = "dashboard"
    else:
        st.session_state.page = "compare"

    # Ubicar opciones avanzadas al final de la barra lateral
    st.divider()
    try:
        with st.popover("⚙️ Opciones de desarrollador"):
            st.caption(f"sklearn: {getattr(sklearn, '__version__', 'N/A')}")
            st.session_state.ae_normal_threshold = st.slider(
                "Umbral Normal (Autoencoder)", min_value=0.0, max_value=1.0, value=0.60, step=0.01,
                help="Si la probabilidad de 'Normal' es mayor o igual al umbral, se clasifica como Normal."
            )
            st.session_state.ae_reconstruction_threshold = st.slider(
                "Umbral Reconstrucción (AE)", min_value=0.0, max_value=1.0, value=0.02, step=0.001,
                help="Si el error de reconstrucción es menor o igual al umbral, se considera normal (junto con el umbral de probabilidad)."
            )
            st.session_state.ocsvm_use_sign = st.toggle(
                "OCSVM: usar predicción por signo",
                value=True,
                help="Usa labels del OCSVM (1=inlier, -1=outlier). Si se desactiva, se usa un umbral sobre decision_function."
            )
            st.session_state.ocsvm_percentile = st.slider(
                "OCSVM percentil umbral", min_value=0.0, max_value=1.0, value=0.45, step=0.01,
                help="Si se usa umbral, clasifica como normal si el score ≥ percentil seleccionado."
            )
            st.divider()
            st.markdown("**🔍 Filtro de Paquetes ARP**")
            st.session_state.arp_limit_mode = st.selectbox(
                "Límite de captura de paquetes ARP",
                options=['low', 'medium', 'high', 'none'],
                index=0,
                format_func=lambda x: {
                    'low': '🟢 Bajo (≈15% ARP)',
                    'medium': '🟡 Medio (≈30% ARP)',
                    'high': '🔴 Alto (≈50% ARP)',
                    'none': '⚪ Sin filtro (todos los paquetes)'
                }.get(x, x),
                help="Controla qué porcentaje de paquetes ARP se capturan. Todos los demás paquetes (TCP, UDP, etc.) se capturan sin límite."
            )
            st.divider()
            st.markdown("**📧 Notificaciones por Correo**")
            st.session_state.enable_email_notifications = st.toggle(
                "Habilitar notificaciones por correo",
                value=st.session_state.get('enable_email_notifications', False),
                help="Solo para capturas automáticas. Las manuales se notifican en la interfaz.",
                key="toggle_email_notifications_1"
            )
            if st.session_state.enable_email_notifications:
                st.session_state.user_email = st.text_input(
                    "Correo de destino",
                    value=st.session_state.get('user_email', ''),
                    placeholder="usuario@gmail.com",
                    help="Correo donde recibirás las notificaciones",
                    key="user_email_input_1"
                )
                st.session_state.gmail_user = st.text_input(
                    "Usuario de Gmail",
                    value=st.session_state.get('gmail_user', ''),
                    placeholder="tucuenta@gmail.com",
                    help="Cuenta de Gmail desde donde se enviarán los emails",
                    key="gmail_user_input_1"
                )
                st.session_state.gmail_app_password = st.text_input(
                    "Contraseña de aplicación Gmail",
                    type="password",
                    value=st.session_state.get('gmail_app_password', ''),
                    help="Genera en: https://myaccount.google.com/apppasswords (no es tu contraseña normal)",
                    key="gmail_app_password_input_1"
                )
                st.info(
                    "📌 **Instrucciones:**\n"
                    "1. Ve a https://myaccount.google.com/apppasswords\n"
                    "2. Asegúrate de tener verificación en 2 pasos activada\n"
                    "3. Selecciona 'Mail' y 'Windows Computer'\n"
                    "4. Copia la contraseña de 16 caracteres y pégala arriba"
                )
                
                # Botones de guardar/limpiar
                col_save, col_clear = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar Configuración", use_container_width=True, key="btn_save_email_config_1"):
                        db = st.session_state.notifications_db
                        success, msg = db.save_email_config(
                            st.session_state.user_email,
                            st.session_state.gmail_user,
                            st.session_state.gmail_app_password
                        )
                        # Guardar también la preferencia
                        db.save_preferences(st.session_state.enable_email_notifications)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                
                with col_clear:
                    if st.button("🗑️ Limpiar Datos", use_container_width=True, key="btn_clear_email_config_1"):
                        db = st.session_state.notifications_db
                        success, msg = db.delete_email_config()
                        if success:
                            st.warning(msg)
                            st.session_state.user_email = ""
                            st.session_state.gmail_user = ""
                            st.session_state.gmail_app_password = ""
                            st.rerun()
                        else:
                            st.error(msg)
    except Exception:
        with st.expander("⚙️ Opciones de desarrollador", expanded=False):
            st.caption(f"sklearn: {getattr(sklearn, '__version__', 'N/A')}")
            st.session_state.ae_normal_threshold = st.slider(
                "Umbral Normal (Autoencoder)", min_value=0.0, max_value=1.0, value=0.60, step=0.01,
                help="Si la probabilidad de 'Normal' es mayor o igual al umbral, se clasifica como Normal."
            )
            st.session_state.ae_reconstruction_threshold = st.slider(
                "Umbral Reconstrucción (AE)", min_value=0.0, max_value=1.0, value=0.02, step=0.001,
                help="Si el error de reconstrucción es menor o igual al umbral, se considera normal (junto con el umbral de probabilidad)."
            )
            st.session_state.ocsvm_use_sign = st.toggle(
                "OCSVM: usar predicción por signo",
                value=True,
                help="Usa labels del OCSVM (1=inlier, -1=outlier). Si se desactiva, se usa un umbral sobre decision_function."
            )
            st.session_state.ocsvm_percentile = st.slider(
                "OCSVM percentil umbral", min_value=0.0, max_value=1.0, value=0.45, step=0.01,
                help="Si se usa umbral, clasifica como normal si el score ≥ percentil seleccionado."
            )
            st.divider()
            st.markdown("**🔍 Filtro de Paquetes ARP**")
            st.session_state.arp_limit_mode = st.selectbox(
                "Límite de captura de paquetes ARP",
                options=['low', 'medium', 'high', 'none'],
                index=0,
                format_func=lambda x: {
                    'low': '🟢 Bajo (≈15% ARP)',
                    'medium': '🟡 Medio (≈30% ARP)',
                    'high': '🔴 Alto (≈50% ARP)',
                    'none': '⚪ Sin filtro (todos los paquetes)'
                }.get(x, x),
                help="Controla qué porcentaje de paquetes ARP se capturan. Todos los demás paquetes (TCP, UDP, etc.) se capturan sin límite."
            )
            st.divider()
            st.markdown("**📧 Notificaciones por Correo**")
            st.session_state.enable_email_notifications = st.toggle(
                "Habilitar notificaciones por correo",
                value=st.session_state.get('enable_email_notifications', False),
                help="Solo para capturas automáticas. Las manuales se notifican en la interfaz.",
                key="toggle_email_notifications_2"
            )
            if st.session_state.enable_email_notifications:
                st.session_state.user_email = st.text_input(
                    "Correo de destino",
                    value=st.session_state.get('user_email', ''),
                    placeholder="usuario@gmail.com",
                    help="Correo donde recibirás las notificaciones",
                    key="user_email_input_2"
                )
                st.session_state.gmail_user = st.text_input(
                    "Usuario de Gmail",
                    value=st.session_state.get('gmail_user', ''),
                    placeholder="tucuenta@gmail.com",
                    help="Cuenta de Gmail desde donde se enviarán los emails",
                    key="gmail_user_input_2"
                )
                st.session_state.gmail_app_password = st.text_input(
                    "Contraseña de aplicación Gmail",
                    type="password",
                    value=st.session_state.get('gmail_app_password', ''),
                    help="Genera en: https://myaccount.google.com/apppasswords (no es tu contraseña normal)",
                    key="gmail_app_password_input_2"
                )
                st.info(
                    "📌 **Instrucciones:**\n"
                    "1. Ve a https://myaccount.google.com/apppasswords\n"
                    "2. Asegúrate de tener verificación en 2 pasos activada\n"
                    "3. Selecciona 'Mail' y 'Windows Computer'\n"
                    "4. Copia la contraseña de 16 caracteres y pégala arriba"
                )
                
                # Botones de guardar/limpiar
                col_save, col_clear = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar Configuración", use_container_width=True, key="btn_save_email_config_2"):
                        db = st.session_state.notifications_db
                        success, msg = db.save_email_config(
                            st.session_state.user_email,
                            st.session_state.gmail_user,
                            st.session_state.gmail_app_password
                        )
                        # Guardar también la preferencia
                        db.save_preferences(st.session_state.enable_email_notifications)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                
                with col_clear:
                    if st.button("🗑️ Limpiar Datos", use_container_width=True, key="btn_clear_email_config_2"):
                        db = st.session_state.notifications_db
                        success, msg = db.delete_email_config()
                        if success:
                            st.warning(msg)
                            st.session_state.user_email = ""
                            st.session_state.gmail_user = ""
                            st.session_state.gmail_app_password = ""
                            st.rerun()
                        else:
                            st.error(msg)

# ...existing code...

#---------------------------------------------------- DASHBOARD ----------------------------------------------------------------------------------------------------------------------------
# DistanceMetric.get_metric("euclidean") devuelve un objeto cuya clase interna
# es la que Python debe encontrar al desempaquetar el pickle.
_dm.EuclideanDistance = DistanceMetric.get_metric("euclidean").__class__


 # RUTAS DE LOS MODELOS

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
    

    # Rutas de modelos permitidos (alineados con el Panel de Control)
    # IFOREST_MODEL_PATHS = "model/iforest__EJERCICIO10_n_components6_fit.pkl"
    # OCSVM_MODEL_PATH = "model/ocsvm__EJERCICIO10_n_components6_fit.pkl"
    # KMEANS_MODEL_PATHS = "model/kmeans1__EJERCICIO10_n_components6_over.pkl"
    # AUTOENCODER_MODEL_PATH = "model/autoencoder.pkl"
    # KMEANS_TXT_PATH = "model/list_kmeans_over.txt"


    # Inicializa el flag una sola vez
    if 'prediccion_realizada' not in st.session_state:
        st.session_state['prediccion_realizada'] = False

    # Estado para captura automática
    if 'auto_capture' not in st.session_state:
        st.session_state.auto_capture = {
            'active': False,
            'is_capturing': False,
            'stop_requested': False,
            'interval_sec': 300,
            'packets_per_capture': 100,
            'duration_sec': 0,  # 0 = sin límite por tiempo
            'next_run_ts': None,
            'last_cycle_result': None,
        }

    # Usar rutas globales: IFOREST_MODEL_PATHS, OCSVM_MODEL_PATH, KMEANS_MODEL_PATHS, AUTOENCODER_MODEL_PATH


    # load_model importado desde backend.model_utils

    col1, col2 = st.columns([1, 2])

    # Columna derecha: bienvenida o resumen tras predicción
    with col2:
        if 'prediccion_realizada' not in st.session_state or not st.session_state['prediccion_realizada']:
            st.markdown("## 👋 Bienvenido al Panel IDS")
            st.info("Aquí verás el resumen y visualización de los resultados una vez realices una predicción. Selecciona el modelo y las opciones en el panel de la izquierda, luego captura paquetes y realiza la predicción.")
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
    
    # Interfas Usuario Panel de Control
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

        # Pestañas justo debajo del formulario (Automática por defecto, Manual)
        tab_auto, tab_manual = st.tabs(["🚀 Captura automática", "🖐️ Captura manual"])

        # ---------------- Captura automática (en pestaña) ----------------
        with tab_auto:
            st.title("⚙️ Captura automática")
            col_auto_a, col_auto_b = st.columns(2)
            with col_auto_a:
                _default_dur_min = max(1, int(st.session_state.auto_capture['duration_sec'] // 60))
                _val_dur_min = st.number_input(
                    'Duración de captura (minutos)', min_value=1, max_value=1440, value=_default_dur_min, step=1,
                    help='La captura automática finalizará cuando se cumpla este tiempo'
                )
                st.session_state.auto_capture['duration_sec'] = int(_val_dur_min * 60)
            with col_auto_b:
                _default_minutes = max(1, int(st.session_state.auto_capture['interval_sec'] // 60))
                _val_minutes = st.number_input(
                    'Intervalo entre capturas (minutos)', min_value=1, max_value=1440, value=_default_minutes, step=1,
                    help='Pausa (en minutos) entre el fin de una captura y el inicio de la siguiente'
                )
                st.session_state.auto_capture['interval_sec'] = int(_val_minutes * 60)
                auto_status = '🟢 Activa' if st.session_state.auto_capture['active'] else '🔴 Detenida'
                st.metric('Estado', auto_status)

            col_btn_a, col_btn_b = st.columns(2)
            with col_btn_a:
                if st.button('▶️ Iniciar automática', use_container_width=True, disabled=st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['active'] = True
                    st.session_state.auto_capture['stop_requested'] = False
                    # Ejecutar inmediatamente la primera
                    st.session_state.auto_capture['next_run_ts'] = time.time()
                    st.rerun()
            with col_btn_b:
                if st.button('⏹️ Detener automática', use_container_width=True, disabled=not st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['stop_requested'] = True
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['next_run_ts'] = None

            # Countdown/estado próximo ciclo
            if st.session_state.auto_capture['active'] and not st.session_state.auto_capture['is_capturing']:
                if st.session_state.auto_capture['next_run_ts'] is not None:
                    remaining = max(0, int(st.session_state.auto_capture['next_run_ts'] - time.time()))
                    if remaining > 0:
                        m, s = divmod(remaining, 60)
                        st.info(f"⏳ Próxima captura en {m:02d}:{s:02d} min:s")
                        # Refrescar para avanzar el conteo
                        time.sleep(1)
                        st.rerun()
        
        
        # Comando y utilidades de captura desde backend.capture_utils
        comm_arg = build_tshark_command()
        
        # Funciones de predicción y métricas importadas desde backend.predict
        
        # mostrar_metricas importado desde backend.predict

        # Función para guardar los paquetes en CSV
        def save_packet_csv(df, path):
            df.to_csv(path, index=False)
            st.success(f"✅ Archivo guardado en {path}")
        
        # Función robusta para limpiar datos
        def clean_data(df):
            """
            Limpia datos de forma exhaustiva para evitar NaN.
            """
            df = df.copy()
            
            # 1. Convertir vacíos a NaN
            df = df.replace(['', 'NaN', 'nan', 'None', 'null'], np.nan)
            
            # 2. Reemplazar comas por puntos en columnas específicas
            lista = ['ip_ttl', 'tos', 'ip_flags_rb', 'ip_flags_df', 'ip_flags_mf']
            for col in lista:
                if col in df.columns:
                    try:
                        df[col] = df[col].astype(str).str.replace(',', '.')
                    except Exception:
                        pass
            
            # 3. Convertir a numérico, reemplazando errores con NaN
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except Exception:
                        pass
            
            # 4. Rellenar NaN con 0
            df = df.fillna(0)
            
            # 5. Reemplazar infinitos con 0
            df = df.replace([np.inf, -np.inf], 0)
            
            # 6. Verificar que NO hay NaN
            if df.isna().any().any():
                st.warning("⚠️ Aún hay valores NaN después de la limpieza, reemplazando con 0...")
                df = df.fillna(0)
            
            return df
            
        # Auxiliar: ejecutar predicción y mostrar resultado (manual/automática)
        def run_prediction_on_data(data_df, is_manual=True):
            try:
                model = None
                if model_option == 'IForest':
                    model = load_model(IFOREST_MODEL_PATHS)
                elif model_option == 'OCSVM':
                    model = load_model(OCSVM_MODEL_PATH)
                elif model_option == 'KMEANS':
                    model = load_model(KMEANS_MODEL_PATHS)
                elif model_option == 'AUTOENCODER':
                    model = load_model(AUTOENCODER_MODEL_PATH)
                if model is None:
                    st.error('No se pudo cargar el modelo seleccionado')
                    return

                # ============ LIMPIEZA ROBUSTA DE DATOS ============
                data_df = clean_data(data_df)
                
                # Verificar que no hay NaN después de limpiar
                nan_count = data_df.isna().sum().sum()
                if nan_count > 0:
                    st.error(f"❌ Error: Aún hay {nan_count} valores NaN después de limpiar")
                    return

                start_time = time.time()
                cpu_usage = psutil.cpu_percent(1)
                mem_usage = psutil.virtual_memory().percent
                disco2 = psutil.disk_usage('/')

                pp3, y_pred, scores = predecir(model, data_df, model_option)
                if pp3 is None or y_pred is None:
                    st.error('Error en la predicción')
                    return

                # Conteos y etiquetas
                if model_option == 'KMEANS':
                    path2 = KMEANS_TXT_PATH
                    dict_pred = dict_predict(path2)
                    etiquetas = [dict_pred.get(int(c), 'Desconocido') for c in y_pred]
                    conteo = Counter(etiquetas)
                    normal_count = conteo.get('Normal',0)
                    ddos_tcp_count = conteo.get('DDoS_TCP',0)
                    ddos_udp_count = conteo.get('DDoS_UDP',0)
                    reconnaissance_count = conteo.get('Reconnaissance',0)
                    total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                    labels = ['Normal','DDOS_TCP','DDOS_UDP','Reconnaissance']
                    values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                    # Calcular porcentaje de anomalías (todo lo que no sea Normal)
                    anomaly_percentage = ((ddos_tcp_count + ddos_udp_count + reconnaissance_count) / total * 100) if total > 0 else 0
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                elif model_option=='AUTOENCODER':
                    normal_count = int(np.count_nonzero(y_pred == 0))
                    ddos_tcp_count = int(np.count_nonzero(y_pred == 1))
                    reconnaissance_count = int(np.count_nonzero(y_pred == 2))
                    ddos_udp_count = int(np.count_nonzero(y_pred == 3))
                    total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                    labels = ['Normal','DDOS_TCP','DDOS_UDP','Reconnaissance']
                    values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                    # Calcular porcentaje de anomalías
                    anomaly_percentage = ((ddos_tcp_count + ddos_udp_count + reconnaissance_count) / total * 100) if total > 0 else 0
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                else:
                    n_normales = int((y_pred == 0).sum())
                    n_anomalos = int((y_pred == 1).sum())
                    total = n_normales + n_anomalos
                    labels = ['Normal','Anómalo']
                    values = [n_normales, n_anomalos]
                    # Calcular porcentaje de anomalías
                    anomaly_percentage = (n_anomalos / total * 100) if total > 0 else 0
                    resumen_text = f"Se analizaron {total} paquetes. Normales: {n_normales}, Anómalos: {n_anomalos}."

                # ============ NOTIFICACIONES ============
                # Actualizar estado y obtener mensaje de alerta
                nm = st.session_state.notification_manager
                nm.update_state(anomaly_percentage)
                is_attack = anomaly_percentage >= 80
                
                # Mostrar notificación en interfaz (toast/alert)
                alert_msg = nm.get_alert_message(anomaly_percentage, is_manual=True)
                if alert_msg['type'] == 'error':
                    st.error(f"{alert_msg['title']}\n{alert_msg['message']}", icon='🚨')
                else:
                    st.success(f"{alert_msg['title']}\n{alert_msg['message']}", icon='✅')
                
                # Enviar email si está habilitado y si debe enviarse
                # Nota: En capturas automáticas se envía; en manuales no
                if st.session_state.get('enable_email_notifications', False) and not is_manual:
                    if nm.should_send_email(is_attack):
                        try:
                            success, msg = nm.send_email(
                                recipient_email=st.session_state.get('user_email', ''),
                                gmail_user=st.session_state.get('gmail_user', ''),
                                gmail_password=st.session_state.get('gmail_app_password', ''),
                                anomaly_percentage=anomaly_percentage,
                                is_manual=is_manual,
                                model_name=model_option
                            )
                            if success:
                                st.toast(f"📧 Email enviado correctamente", icon='✉️')
                            else:
                                st.warning(f"⚠️ Error enviando email: {msg}")
                        except Exception as e:
                            st.warning(f"⚠️ Error al enviar email: {str(e)}")
                
                # Guardar estado para el panel derecho
                st.session_state['prediccion_realizada'] = True
                st.session_state['resumen_prediccion'] = {'texto': resumen_text, 'labels': labels, 'values': values}
                st.session_state.data = data_df

                # Visual de resultados mínima
                st.markdown("### 📊 Paquetes capturados")
                st.dataframe(data_df)

                # Colores: verde para Normal, rojo para el resto (ataques)
                bar_colors = [('#00C853' if (str(lbl).lower() == 'normal') else '#FF5252') for lbl in labels]
                fig = go.Figure(data=[go.Bar(x=labels, y=values, text=values, textposition='auto', marker_color=bar_colors)])
                fig.update_layout(title='Distribución de Detecciones', title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)

                # Diagnóstico adicional para OCSVM: distribución de scores y umbral
                if model_option == 'OCSVM' and isinstance(scores, (np.ndarray, list)) and len(scores) > 0:
                    try:
                        thr = None
                        if not st.session_state.get('ocsvm_use_sign', True):
                            pct = float(st.session_state.get('ocsvm_percentile', 0.45))
                            thr = np.percentile(scores, 100 * pct)
                        hist_fig = go.Figure()
                        hist_fig.add_trace(go.Histogram(x=scores, nbinsx=30, marker_color='#4B9FE1', name='decision_function'))
                        if thr is not None:
                            hist_fig.add_shape(type='line', x0=thr, x1=thr, y0=0, y1=1, xref='x', yref='paper', line=dict(color='#FF5252', width=2))
                            hist_fig.add_annotation(x=thr, y=1, yref='paper', text=f"Umbral={thr:.3f}", showarrow=True, arrowhead=1)
                        hist_fig.update_layout(title='OCSVM: distribución de decision_function', title_x=0.5)
                        st.plotly_chart(hist_fig, use_container_width=True)
                    except Exception:
                        pass

                if metric_option == 'Internas':
                    unique_labels = np.unique(y_pred)
                    if len(unique_labels) >= 2:
                        silhouette, calinski, davies = metricas.metrica_internas(pp3, y_pred)
                        mostrar_metricas(silhouette, calinski, davies)
                    else:
                        st.info("Las métricas internas requieren al menos dos clases en la predicción. Actualmente todas las muestras pertenecen a una sola clase.")

                # Métricas de recursos
                tiempo_total = time.time() - start_time
                met_cols = st.columns(4)
                with met_cols[0]:
                    st.metric("⏱️ Tiempo (s)", f"{tiempo_total:.2f}")
                with met_cols[1]:
                    st.metric("🖥️ % CPU", f"{cpu_usage:.2f}%")
                with met_cols[2]:
                    st.metric("💾 % Memoria", f"{mem_usage:.2f}%")
                with met_cols[3]:
                    st.metric("📀 % Disco", f"{disco2[3]:.2f}%")

            except Exception as e:
                st.error(f"❌ Error en la predicción automática: {str(e)}")

        # Streamlit UI (contenido de pestañas)

        data = None  # Inicializamos el DataFrame

        # ---------------- Pestaña: Captura manual ----------------
        with tab_manual:
            st.title("🖐️ Captura manual")

            # Parámetros manuales
            col_man_a, col_man_b = st.columns(2)
            with col_man_a:
                manual_packets = st.number_input('Paquetes a capturar (manual)', min_value=10, max_value=50000, value=100, step=10)
            with col_man_b:
                manual_duration_min = st.number_input('Duración máx. (min) (manual)', min_value=0, max_value=1440, value=0, step=1)
            manual_duration = int(manual_duration_min * 60)
           
            if st.button("🚀 Iniciar Captura", key="btn_manual_capture"):
                process = capturing_packets(comm_arg)
                st.write("📡 Capturando paquetes...")

                # Inicializamos el DataFrame
                captured_data = None
                progress_bar = st.progress(0, text="Capturando paquetes...")
                total_packets = manual_packets
                start_ts = time.time()
                arp_mode = st.session_state.get('arp_limit_mode', 'low')
                arp_count = 0
                packets_count = 0

                while packets_count < total_packets:
                    # Parar por tiempo si está configurado
                    if manual_duration and (time.time() - start_ts) >= manual_duration:
                        break
                    packet_str = process.stdout.readline().strip()
                    if packet_str:
                        packet_list = packet_str.split("\t")
                        protocol = packet_list[1] if len(packet_list) > 1 else ''
                        
                        # Usar el filtro ARP en tiempo real
                        accept_packet = apply_realtime_arp_filter(protocol, arp_count, packets_count, arp_mode)
                        
                        if accept_packet:
                            type_packet_data = type_packet(packet_list)
                            captured_data = packet_df(type_packet_data, captured_data)
                            if protocol == 'ARP':
                                arp_count += 1
                            packets_count += 1
                            progress_bar.progress(packets_count / total_packets, text=f"Paquetes capturados: {packets_count}/{total_packets} (ARP: {arp_count})")

                try:
                    process.terminate()
                except Exception:
                    pass
                progress_bar.empty()
                st.success("✅ Captura finalizada.")
                
                if arp_mode != 'none':
                    st.info(f"📊 Estadísticas de captura: {packets_count - arp_count} paquetes útiles + {arp_count} paquetes ARP = {packets_count} total")

                # Mostrar el DataFrame capturado y permitir guardar
                if captured_data is not None and list(captured_data.columns) != ['value']:
                    st.write("📊 *Paquetes capturados:*")
                    st.dataframe(captured_data)
                    st.session_state.data = captured_data
                    st.success("Datos capturados listos para predicción")
                    if st.button("💾 Guardar en CSV"):
                        save_packet_csv(captured_data, "captura_paquetes.csv")

        # ---------------- Pestaña: Captura automática ----------------
        with tab_auto:
            # Ejecución automática si está activa y toca ciclo
            if st.session_state.auto_capture['active'] and not st.session_state.auto_capture['is_capturing']:
                due = st.session_state.auto_capture['next_run_ts'] is not None and time.time() >= st.session_state.auto_capture['next_run_ts']
                if due:
                    st.session_state.auto_capture['is_capturing'] = True
                    st.info('🚀 Ejecutando captura automática...')
                    process = capturing_packets(comm_arg)

                    captured_data = None
                    duration_sec = int(st.session_state.auto_capture['duration_sec'])
                    if duration_sec <= 0:
                        duration_sec = 60
                    start_ts = time.time()
                    end_ts = start_ts + duration_sec
                    prog = st.progress(0, text='Capturando (automática)...')
                    
                    arp_mode = st.session_state.get('arp_limit_mode', 'low')
                    arp_count = 0
                    packets_count = 0
                    
                    while time.time() < end_ts:
                        if st.session_state.auto_capture['stop_requested']:
                            break
                        packet_str = process.stdout.readline().strip()
                        if packet_str:
                            packet_list = packet_str.split('\t')
                            protocol = packet_list[1] if len(packet_list) > 1 else ''
                            
                            # Usar el filtro ARP en tiempo real
                            accept_packet = apply_realtime_arp_filter(protocol, arp_count, packets_count, arp_mode)
                            
                            if accept_packet:
                                type_packet_data = type_packet(packet_list)
                                captured_data = packet_df(type_packet_data, captured_data)
                                if protocol == 'ARP':
                                    arp_count += 1
                                packets_count += 1
                        
                        elapsed = time.time() - start_ts
                        frac = min(1.0, elapsed / duration_sec)
                        prog.progress(frac, text=f"Tiempo: {int(elapsed)}s / {duration_sec}s (Paquetes: {packets_count}, ARP: {arp_count})")
                    
                    try:
                        process.terminate()
                    except Exception:
                        pass
                    prog.empty()

                    if st.session_state.auto_capture['stop_requested']:
                        st.warning('⏹️ Captura automática detenida por el usuario.')
                        st.session_state.auto_capture['active'] = False
                        st.session_state.auto_capture['is_capturing'] = False
                        st.session_state.auto_capture['next_run_ts'] = None
                    else:
                        if captured_data is not None and list(captured_data.columns) != ['value']:
                            if arp_mode != 'none':
                                st.info(f"📊 Captura completada: {packets_count - arp_count} paquetes útiles + {arp_count} ARP = {packets_count} total")
                            st.success('✅ Captura automática finalizada. Ejecutando predicción...')
                            st.session_state.data = captured_data
                            run_prediction_on_data(captured_data, is_manual=False)
                        # Programar siguiente ciclo y relanzar el countdown
                        st.session_state.auto_capture['next_run_ts'] = time.time() + int(st.session_state.auto_capture['interval_sec'])
                        st.session_state.auto_capture['is_capturing'] = False
                        st.rerun()

        # Sección de carga de archivo CSV
        uploaded_file = None  # Evita UnboundLocalError si no se usa el cargador
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
                    try:
                        data = pd.read_csv(uploaded_file)
                        if data.empty or data.shape[1] == 0:
                            st.error("❌ El archivo CSV está vacío o no contiene columnas válidas.")
                            data = None
                        else:
                            st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos cargados exitosamente</div>', unsafe_allow_html=True)
                            
                            with st.expander("📊 Vista previa de datos"):
                                st.dataframe(data.head())
                                st.info(f"Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")
                    except pd.errors.EmptyDataError:
                        st.error("❌ El archivo CSV está vacío o no tiene columnas válidas.")
                        data = None
                    except Exception as e:
                        st.error(f"❌ Error al cargar el archivo: {str(e)}")
                        data = None
                else:
                    data = None

        if st.button('🚀 Realizar Predicción', key='predict'):
            if data is not None:
                run_prediction_on_data(data)
            else:
                st.warning("⚠ Por favor capture paquetes o cargue un archivo CSV antes de realizar la predicción.")

        # Descargar reporte PDF de la última predicción
        st.markdown("### 📄 Descargar Reporte PDF")
        if st.session_state.get('prediccion_realizada') and 'resumen_prediccion' in st.session_state:
            resumen = st.session_state['resumen_prediccion']
            # Crear gráfica de barras solo para el PDF (no afecta la UI de torta)
            fig_bar, ax = plt.subplots(figsize=(6, 3.5))
            bar_colors = [('#00C853' if (str(lbl).lower() == 'normal') else '#FF5252') for lbl in resumen['labels']]
            ax.bar(resumen['labels'], resumen['values'], color=bar_colors)
            ax.set_title('Distribución de Detecciones')
            ax.set_ylabel('Cantidad')
            for i, v in enumerate(resumen['values']):
                ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=10)
            plt.tight_layout()

            pdf_bytes = generar_reporte_pdf(
                resumen=resumen['texto'],
                labels=resumen['labels'],
                values=resumen['values'],
                descripcion_amenazas=DESCRIPCIONES_AMENAZAS,
                fig=fig_bar
            )
            st.download_button(
                label="📄 Descargar reporte PDF",
                data=pdf_bytes,
                file_name="reporte_prediccion_IDS.pdf",
                mime="application/pdf"
            )
            plt.close(fig_bar)
        else:
            st.warning("⚠ Primero debes capturar tráfico o hacer una predicción antes de descargar el reporte.") 
        
    

    # Nota: Bloque antiguo de predicción con archivo subido eliminado por duplicado y uso de modelos no permitidos.


# Control de navegación
def show_compare_page():
    st.title('📊 Comparar Modelos')
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.06); padding: 1rem 1.2rem; border-radius: 12px; margin: .6rem 0 1rem 0;">
        <p style="margin:0; font-size: .95rem; line-height:1.5;">
        • Seleccione uno o varios modelos para ejecutar la misma predicción sobre un único conjunto de datos (última captura o un CSV).<br/>
        • <strong>Internas</strong>: calcula Silhouette, Calinski y Davies sobre las representaciones del pipeline si hay ≥2 clases predichas.<br/>
        • <strong>Externas</strong>: requiere una columna con etiquetas reales; para modelos multiclase (KMEANS/Autoencoder) se resume a <em>Normal</em> vs <em>Ataque</em> para AUC/ROC.<br/>
        • El gráfico "Normal vs Ataques" suma todas las categorías de ataque (p. ej., DDoS_TCP/UDP, Reconnaissance).
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    src_cols = st.columns(2)
    data_source = None
    if 'data' in st.session_state and st.session_state.data is not None:
        with src_cols[0]:
            usar_captura = st.checkbox('Usar datos de la última captura', value=True)
        if usar_captura:
            data_source = st.session_state.data.copy()
    if data_source is None:
        with src_cols[1]:
            uploaded_cmp = st.file_uploader('Cargar CSV para comparar', type='csv', key='csv_compare')
        if uploaded_cmp is not None:
            data_source = pd.read_csv(uploaded_cmp)
            st.success('Datos cargados para comparar.')
        else:
            st.info('Cargue un CSV o use la última captura para habilitar la comparación.')

    st.markdown('#### Modelos a comparar')
    model_choices = ['IForest', 'OCSVM', 'KMEANS', 'AUTOENCODER']
    selected_models = st.multiselect('Seleccione modelos', model_choices, default=['IForest','OCSVM','KMEANS'])

    metric_compare = st.selectbox('Métricas de validación', ['Internas', 'Externas', 'Ninguna'], help='Internas: Silhouette, Calinski, Davies. Externas: requiere columna de etiquetas reales.')

    true_label_col = None
    if metric_compare == 'Externas':
        if data_source is not None:
            posibles = data_source.columns.tolist()
            true_label_col = st.selectbox('Columna de etiquetas reales (0/1 o multiclase)', posibles)
        else:
            st.info('Cargue datos con etiquetas reales para métricas externas.')

    def _prep_df(df: pd.DataFrame) -> pd.DataFrame:
        lista = ['ip_ttl','tos','ip_flags_rb','ip_flags_df','ip_flags_mf']
        df = df.copy()
        
        # Convertir vacíos a NaN
        df = df.replace(['', 'NaN', 'nan', 'None', 'null'], np.nan)
        
        # Reemplazar comas por puntos
        if set(lista).issubset(set(df.columns)):
            df[lista] = df[lista].astype('str')
            df.ip_ttl = df.ip_ttl.str.replace(',', '.')
            df.tos = df.tos.str.replace(',', '.')
            df.ip_flags_rb = df.ip_flags_rb.str.replace(',', '.')
            df.ip_flags_df = df.ip_flags_df.str.replace(',', '.')
            df.ip_flags_mf = df.ip_flags_mf.str.replace(',', '.')
        
        # Convertir a numérico
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception:
                    pass
        
        # Rellenar NaN e infinitos
        df = df.replace([np.inf, -np.inf], 0)
        return df.fillna(0)

    def _load(opt: str):
               return {
            'IForest': IFOREST_MODEL_PATHS,
            'OCSVM': OCSVM_MODEL_PATH,
            'KMEANS': KMEANS_MODEL_PATHS,
            'AUTOENCODER': AUTOENCODER_MODEL_PATH,
        }.get(opt)

    def _predict(opt: str, model, df: pd.DataFrame):
        try:
            if opt == 'IForest':
                scores = model.decision_function(df)
                y = pred_threshold(scores, -0.10)['Pred'].values
                pp3 = model[0].transform(df)
            # LOF no permitido
            elif opt == 'OCSVM':
                scores = model.decision_function(df)
                thr = np.percentile(scores, 100 * 0.45)
                y = np.where(scores >= thr, 0, 1)
                pp3 = model[0].transform(df)
            elif opt == 'KMEANS':
                y = model.predict(df)
                pp3 = model[0].transform(df)
            # DBSCAN no permitido
            elif opt == 'AUTOENCODER':
                y = model.predict(df)
                pp3 = model[0].transform(df)
            else:
                return None, None
            return pp3, y
        except Exception:
            return None, None

    def _counts(opt: str, y):
        if y is None:
            return {'Normal': 0, 'Anómalo': 0, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}
        if opt in ['KMEANS']:
            path2 = KMEANS_TXT_PATH
            mapping = dict_predict(path2)
            etiquetas = [mapping.get(int(c), 'Desconocido') for c in y]
            c = Counter(etiquetas)
            return {
                'Normal': int(c.get('Normal', 0)),
                'Anómalo': int(c.get('Anómalo', 0)),
                'DDOS_TCP': int(c.get('DDoS_TCP', 0)),
                'DDOS_UDP': int(c.get('DDoS_UDP', 0)),
                'Reconnaissance': int(c.get('Reconnaissance', 0)),
            }
        if opt == 'AUTOENCODER':
            return {
                'Normal': int(np.count_nonzero(y == 0)),
                'Anómalo': 0,
                'DDOS_TCP': int(np.count_nonzero(y == 1)),
                'DDOS_UDP': int(np.count_nonzero(y == 3)),
                'Reconnaissance': int(np.count_nonzero(y == 2)),
            }
        normales = int((y == 0).sum())
        anomalos = int((y == 1).sum())
        return {'Normal': normales, 'Anómalo': anomalos, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}

    if st.button('🚀 Comparar'):
        if data_source is None:
            st.warning('⚠ Cargue datos o use la última captura antes de comparar.')
            return
        dfp = _prep_df(data_source)
        y_true = None
        if metric_compare == 'Externas' and true_label_col is not None and true_label_col in data_source.columns:
            y_true = data_source[true_label_col].values
        filas = []
        for opt in selected_models:
            path = _load(opt)
            if path is None:
                st.error(f'Ruta no definida para {opt}')
                continue
            model = load_model(path)
            if model is None:
                st.error(f'No se pudo cargar el modelo {opt}')
                continue
            t0 = time.time()
            pp3, y = _predict(opt, model, dfp)
            pred_time = time.time() - t0
            conteos = _counts(opt, y)
            fila = {'Modelo': opt, **conteos, 'Tiempo (s)': float(pred_time)}
            if metric_compare == 'Internas' and y is not None and len(np.unique(y)) >= 2:
                try:
                    s, c, d = metricas.metrica_internas(pd.DataFrame(pp3), y)
                    fila.update({'Silhouette': float(s), 'Calinski': float(c), 'Davies': float(d)})
                except Exception:
                    fila.update({'Silhouette': None, 'Calinski': None, 'Davies': None})
            if metric_compare == 'Externas' and y_true is not None and y is not None and len(y_true) == len(y):
                try:
                    from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
                    # Si y es multiclase, intentamos binarizar para ROC (Normal=0 vs resto=1)
                    y_bin = None
                    if opt in ['KMEANS']:
                        # mapear etiquetas a binario: Normal=0, otros=1
                        path2 = KMEANS_TXT_PATH
                        mapping = dict_predict(path2)
                        etiquetas = np.array([mapping.get(int(c), 'Desconocido') for c in y])
                        y_bin = (etiquetas != 'Normal').astype(int)
                    elif opt == 'AUTOENCODER':
                        y_bin = (y != 0).astype(int)
                    else:
                        y_bin = y.astype(int)

                    # confusión
                    cm = confusion_matrix(y_true, y_bin)
                    fila.update({'MatrizConfusion': cm})

                    # ROC AUC si y_true es binario
                    if np.unique(y_true).size == 2 and np.unique(y_bin).size == 2:
                        try:
                            aucv = roc_auc_score(y_true, y_bin)
                            fila.update({'ROC_AUC': float(aucv)})
                        except Exception:
                            pass
                except Exception:
                    pass
            filas.append(fila)

        if not filas:
            st.info('Sin resultados para mostrar.')
            return

        res_df = pd.DataFrame(filas)
        cols = ['Modelo', 'Normal', 'Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance', 'Tiempo (s)']
        if metric_compare == 'Internas':
            cols += ['Silhouette', 'Calinski', 'Davies']
        if metric_compare == 'Externas':
            cols += ['ROC_AUC']
        st.markdown('### 📋 Resumen')
        st.dataframe(res_df[cols], use_container_width=True)

        if metric_compare == 'Externas':
            st.markdown('### 🧮 Matrices de Confusión')
            for _, row in res_df.iterrows():
                if 'MatrizConfusion' in row and row['MatrizConfusion'] is not None:
                    st.write(f"Modelo: {row['Modelo']}")
                    st.dataframe(pd.DataFrame(row['MatrizConfusion']), use_container_width=True)

        st.markdown('### 📊 Normal vs Ataques')
        modelos = res_df['Modelo']
        normales = res_df['Normal']
        ataques = (res_df['Anómalo'].fillna(0) + res_df['DDOS_TCP'].fillna(0) + res_df['DDOS_UDP'].fillna(0) + res_df['Reconnaissance'].fillna(0))
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Normal', x=modelos, y=normales, marker_color='#00C853'))
        fig.add_trace(go.Bar(name='Ataques', x=modelos, y=ataques, marker_color='#FF5252'))
        fig.update_layout(barmode='group', title='Normal vs Ataques por modelo', title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico ligero de tiempos
        if 'Tiempo (s)' in res_df.columns:
            st.markdown('### ⏱️ Tiempos de predicción por modelo')
            figt = go.Figure(data=[go.Bar(x=res_df['Modelo'], y=res_df['Tiempo (s)'], marker_color='#4B9FE1')])
            figt.update_layout(title='Tiempo de predicción (s)', title_x=0.5)
            st.plotly_chart(figt, use_container_width=True)

if st.session_state.page == "home":
    show_home_page()
elif st.session_state.page == "dashboard":
    show_dashboard_page()
else:
    show_compare_page()

# Pie de página mejorado
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🛡 Sistema de Detección de Anomalías IoT</p>
            <p>© 2025 Innovasic | UCC</p>
        </div>
        """,
        unsafe_allow_html=True)

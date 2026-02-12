"""
Frontend Ligero para IDS IoT
Ejecutar en Streamlit Cloud - consume API del backend en Raspberry Pi
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import os
from pathlib import Path

# Configuración
st.set_page_config(
    page_title="IDS IoT - Sistema de Detección de Intrusiones",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL del backend API (configurable via variable de entorno)
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# ==================== ESTILOS ====================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .status-online {
        color: #10b981;
        font-weight: bold;
    }
    .status-offline {
        color: #ef4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES DE API ====================

def check_backend_health():
    """Verifica si el backend está disponible"""
    try:
        response = requests.get(f"{BACKEND_API_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def get_system_metrics():
    """Obtiene métricas del sistema desde el backend"""
    try:
        response = requests.get(f"{BACKEND_API_URL}/metrics", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error obteniendo métricas: {e}")
        return None

def capture_packets(duration, arp_filter_mode='low'):
    """Inicia captura de paquetes"""
    try:
        payload = {
            "duration": duration,
            "arp_filter_mode": arp_filter_mode
        }
        response = requests.post(
            f"{BACKEND_API_URL}/capture",
            json=payload,
            timeout=duration + 30  # timeout mayor a la duración
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en captura: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error en captura: {e}")
        return None

def predict_anomalies(data, model_name, config=None):
    """Envía datos al backend para predicción"""
    try:
        payload = {
            "data": data,
            "model_name": model_name,
            "metric_type": "Internas",
            "config": config or {}
        }
        response = requests.post(
            f"{BACKEND_API_URL}/predict",
            json=payload,
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en predicción: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error en predicción: {e}")
        return None

def get_available_models():
    """Lista modelos disponibles en el backend"""
    try:
        response = requests.get(f"{BACKEND_API_URL}/models", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error obteniendo modelos: {e}")
        return None

# ==================== SIDEBAR ====================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/security-shield-green.png", width=80)
    st.title("🛡️ IDS IoT")
    
    # Status del backend
    st.markdown("---")
    st.subheader("Estado del Backend")
    
    is_online, health_data = check_backend_health()
    
    if is_online:
        st.markdown('<p class="status-online">🟢 Conectado</p>', unsafe_allow_html=True)
        st.caption(f"Raspberry Pi: {BACKEND_API_URL}")
    else:
        st.markdown('<p class="status-offline">🔴 Desconectado</p>', unsafe_allow_html=True)
        st.error("No se puede conectar con el backend. Verifica que esté ejecutándose.")
        st.code(f"python backend_api.py", language="bash")
        st.stop()
    
    # Navegación
    st.markdown("---")
    page = st.radio(
        "Navegación",
        ["📊 Panel de Control", "🔍 Captura Manual", "📈 Métricas del Sistema"],
        label_visibility="collapsed"
    )

# ==================== PÁGINA PRINCIPAL ====================

if page == "📊 Panel de Control":
    st.markdown('<h1 class="main-header">🛡️ Panel de Control - IDS IoT</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Captura y Análisis Automático")
        
        # Configuración de captura
        with st.expander("⚙️ Configuración", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                duration = st.slider("Duración de captura (segundos)", 30, 300, 60)
                model_selected = st.selectbox(
                    "Modelo de detección",
                    ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"]
                )
            with col_b:
                arp_filter = st.select_slider(
                    "Filtro de paquetes ARP",
                    options=['none', 'low', 'medium', 'high'],
                    value='low'
                )
                auto_refresh = st.toggle("Auto-refresh al finalizar", value=False)
        
        if st.button("🚀 Iniciar Captura y Análisis", type="primary", use_container_width=True):
            with st.spinner(f"📡 Capturando paquetes por {duration} segundos..."):
                # Barra de progreso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                start_time = time.time()
                
                # Iniciar captura (esto bloqueará hasta que termine)
                capture_result = capture_packets(duration, arp_filter)
                
                if capture_result and capture_result['status'] == 'success':
                    st.success(f"✅ Captura completada: {capture_result['packets_captured']} paquetes")
                    
                    # Guardar en session_state
                    st.session_state.last_capture = capture_result
                    
                    # Realizar predicción
                    with st.spinner(f"🔮 Analizando con {model_selected}..."):
                        prediction_result = predict_anomalies(
                            capture_result['data'],
                            model_selected,
                            config={
                                'ae_normal_threshold': 0.60,
                                'ocsvm_percentile': 0.45
                            }
                        )
                        
                        if prediction_result and prediction_result['status'] == 'success':
                            st.session_state.last_prediction = prediction_result
                            st.success("✅ Análisis completado")
                            
                            if auto_refresh:
                                st.rerun()
                else:
                    st.error("❌ Error en la captura")
    
    with col2:
        st.subheader("Estado del Sistema")
        metrics = get_system_metrics()
        if metrics:
            st.metric("🖥️ CPU", f"{metrics['cpu_percent']:.1f}%")
            st.metric("💾 Memoria", f"{metrics['memory_percent']:.1f}%")
            st.metric("💽 Disco", f"{metrics['disk_usage_percent']:.1f}%")
            
            with st.expander("Interfaces de red"):
                for iface in metrics['network_interfaces']:
                    st.text(f"• {iface}")
    
    # Mostrar resultados si existen
    st.markdown("---")
    
    if 'last_prediction' in st.session_state:
        pred = st.session_state.last_prediction
        
        st.subheader("📊 Resultados del Análisis")
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div class="metric-value">{pred['n_normal']}</div>
                <div class="metric-label">Tráfico Normal</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-value">{pred['n_anomalous']}</div>
                <div class="metric-label">Anomalías Detectadas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total = pred['n_normal'] + pred['n_anomalous']
            pct = (pred['n_anomalous'] / total * 100) if total > 0 else 0
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metric-value">{pct:.1f}%</div>
                <div class="metric-label">Tasa de Anomalías</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de distribución
        st.markdown("### 📈 Distribución de Tráfico")
        
        fig = go.Figure(data=[
            go.Pie(
                labels=['Normal', 'Anomalías'],
                values=[pred['n_normal'], pred['n_anomalous']],
                hole=.4,
                marker_colors=['#10b981', '#ef4444']
            )
        ])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas internas si existen
        if pred.get('metrics'):
            st.markdown("### 📊 Métricas de Clustering")
            m = pred['metrics']
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Silhouette Score", f"{m['silhouette']:.4f}")
            col2.metric("Calinski-Harabasz", f"{m['calinski_harabasz']:.2f}")
            col3.metric("Davies-Bouldin", f"{m['davies_bouldin']:.4f}")

elif page == "🔍 Captura Manual":
    st.markdown('<h1 class="main-header">🔍 Captura Manual de Paquetes</h1>', unsafe_allow_html=True)
    
    st.info("💡 Realiza capturas personalizadas con control total sobre los parámetros")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        duration = st.number_input("Duración (segundos)", min_value=10, max_value=600, value=60)
        arp_mode = st.selectbox(
            "Filtro ARP",
            options=['none', 'low', 'medium', 'high'],
            format_func=lambda x: {
                'none': '⚪ Sin filtro',
                'low': '🟢 Bajo (≈15%)',
                'medium': '🟡 Medio (≈30%)',
                'high': '🔴 Alto (≈50%)'
            }.get(x, x)
        )
    
    with col2:
        model_choice = st.selectbox("Modelo ML", ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"])
        
        if model_choice == "AUTOENCODER":
            ae_threshold = st.slider("Umbral Normal", 0.0, 1.0, 0.60, 0.01)
        elif model_choice == "OCSVM":
            ocsvm_pct = st.slider("Percentil", 0.0, 1.0, 0.45, 0.01)
    
    if st.button("▶️ Ejecutar Captura", type="primary", use_container_width=True):
        with st.spinner("Capturando..."):
            result = capture_packets(duration, arp_mode)
            
            if result:
                st.success(f"✅ {result['packets_captured']} paquetes capturados")
                
                # Análisis
                config = {}
                if model_choice == "AUTOENCODER":
                    config['ae_normal_threshold'] = ae_threshold
                elif model_choice == "OCSVM":
                    config['ocsvm_percentile'] = ocsvm_pct
                
                with st.spinner("Analizando..."):
                    pred = predict_anomalies(result['data'], model_choice, config)
                    
                    if pred:
                        st.balloons()
                        st.markdown("### Resultados")
                        
                        col1, col2 = st.columns(2)
                        col1.metric("✅ Normal", pred['n_normal'])
                        col2.metric("⚠️ Anomalías", pred['n_anomalous'])
                        
                        # Tabla de datos
                        with st.expander("Ver datos capturados"):
                            df = pd.DataFrame(result['data'])
                            df['prediction'] = pred['predictions']
                            st.dataframe(df, use_container_width=True)

elif page == "📈 Métricas del Sistema":
    st.markdown('<h1 class="main-header">📈 Métricas del Sistema</h1>', unsafe_allow_html=True)
    
    if st.button("🔄 Actualizar Métricas"):
        st.rerun()
    
    metrics = get_system_metrics()
    
    if metrics:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Recursos del Sistema")
            
            # CPU
            fig_cpu = go.Figure(go.Indicator(
                mode="gauge+number",
                value=metrics['cpu_percent'],
                title={'text': "CPU (%)"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 80], 'color': "yellow"},
                           {'range': [80, 100], 'color': "red"}
                       ]}
            ))
            fig_cpu.update_layout(height=250)
            st.plotly_chart(fig_cpu, use_container_width=True)
            
            # Memoria
            fig_mem = go.Figure(go.Indicator(
                mode="gauge+number",
                value=metrics['memory_percent'],
                title={'text': "Memoria (%)"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "green"},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 80], 'color': "yellow"},
                           {'range': [80, 100], 'color': "red"}
                       ]}
            ))
            fig_mem.update_layout(height=250)
            st.plotly_chart(fig_mem, use_container_width=True)
        
        with col2:
            st.subheader("Información del Sistema")
            
            st.metric("💾 Memoria Disponible", f"{metrics['memory_available_mb']:.0f} MB")
            st.metric("💽 Uso de Disco", f"{metrics['disk_usage_percent']:.1f}%")
            
            st.markdown("#### Interfaces de Red")
            for iface in metrics['network_interfaces']:
                st.info(f"🔌 {iface}")
            
            st.markdown("#### Modelos Cargados")
            models_info = get_available_models()
            if models_info:
                for model in models_info['available_models']:
                    st.success(f"✅ {model}")

# ==================== FOOTER ====================

st.markdown("---")
st.caption(f"🛡️ IDS IoT v1.0 | Backend: {BACKEND_API_URL}")

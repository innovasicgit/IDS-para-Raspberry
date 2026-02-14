"""
Página principal del dashboard - Panel de Control de Detección.
"""

import streamlit as st
from config.theme import get_current_theme
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import matplotlib.pyplot as plt
from collections import Counter
import psutil
import os
import requests

from backend.constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH,
)
from backend.model_utils import load_model, dict_predict, pred_threshold
from backend.capture_utils import (
    build_tshark_command,
    capturing_packets,
    type_packet,
    packet_df,
)
from backend.predict import predecir, mostrar_metricas
from frontend.pdf_report import generar_reporte_pdf, DESCRIPCIONES_AMENAZAS
from frontend.analysis_explanations import (
    explicar_distribucion,
    explicar_metricas_rendimiento,
    explicar_patron_trafico,
    generar_resumen_general
)
import metricas
# Detectar si estamos en Streamlit Cloud o local
def is_streamlit_cloud():
    """Detecta si la app está corriendo en Streamlit Cloud"""
    return os.getenv('STREAMLIT_SHARING_MODE') is not None or \
           os.path.exists('/mount/src')

# URL del backend API (debe configurarse en secrets o .env)
def get_backend_url():
    """Obtiene la URL del backend desde secrets o variable de entorno"""
    # Primero intentar desde secrets de Streamlit
    try:
        return st.secrets.get("BACKEND_URL", "https://reviewed-sailing-grid-clinic.trycloudflare.com")
    except:
        # Fallback a variable de entorno o URL por defecto
        return os.getenv("BACKEND_URL", "https://reviewed-sailing-grid-clinic.trycloudflare.com")

def capture_via_api(duration_sec, backend_url):
    """
    Captura paquetes usando el backend API
    
    Args:
        duration_sec: Duración de la captura en segundos
        backend_url: URL del backend API
        
    Returns:
        DataFrame con los paquetes capturados o None si hay error
    """
    try:
        response = requests.post(
            f"{backend_url}/capture",
            json={
                "duration": duration_sec,
                "arp_filter_mode": "none"
            },
            timeout=duration_sec + 30  # Timeout mayor a la duración
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success' and result['data']:
                df = pd.DataFrame(result['data'])
                return df
            else:
                st.error(f"No se capturaron paquetes")
                return None
        else:
            st.error(f"Error en la captura: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout: La captura tomó demasiado tiempo")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Error de conexión: No se pudo conectar al backend. Verifica que el backend esté corriendo y la URL sea correcta.")
        return None
    except Exception as e:
        st.error(f"❌ Error en la captura: {str(e)}")
        return None

def capture_local(duration_sec, comm_arg):
    """
    Captura paquetes usando tshark local (solo para ejecución local)
    
    Args:
        duration_sec: Duración de la captura en segundos
        comm_arg: Comando tshark construido
        
    Returns:
        DataFrame con los paquetes capturados
    """
    process = capturing_packets(comm_arg)
    captured_data = None
    start_ts = time.time()
    end_ts = start_ts + duration_sec
    
    while time.time() < end_ts:
        packet_str = process.stdout.readline().strip()
        if packet_str:
            packet_list = packet_str.split('\t')
            type_packet_data = type_packet(packet_list)
            captured_data = packet_df(type_packet_data, captured_data)
    
    try:
        process.terminate()
    except Exception:
        pass
        
    return captured_data

def show_dashboard_page():
    """Página principal del dashboard."""

    t = get_current_theme()
    c = t.colors
    
    # Título con botón de descarga PDF en la misma línea
    col_title, col_pdf = st.columns([3, 1])
    with col_title:
        st.title('🎯 Panel de Control de Detección')
    with col_pdf:
        # Botón de descarga PDF en la esquina superior derecha
        if st.session_state.get('prediccion_realizada') and 'resumen_prediccion' in st.session_state:
            resumen = st.session_state['resumen_prediccion']
            # Crear gráfica de barras para el PDF
            fig_bar, ax = plt.subplots(figsize=(6, 3.5))
            bar_colors = [(c.success if (str(lbl).lower() == 'normal') else c.error) for lbl in resumen['labels']]
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
                label="📄 Descargar PDF",
                data=pdf_bytes,
                file_name="reporte_prediccion_IDS.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            plt.close(fig_bar)
        else:
            st.button(
                "📄 Descargar PDF",
                disabled=True,
                use_container_width=True,
                help="⚠ Primero debes capturar tráfico o hacer una predicción antes de descargar el reporte."
            )

    # Inicializa el flag una sola vez
    if 'prediccion_realizada' not in st.session_state:
        st.session_state['prediccion_realizada'] = False

    # Estado para captura automática
    if 'auto_capture' not in st.session_state:
        st.session_state.auto_capture = {
            'active': False,
            'is_capturing': False,
            'stop_requested': False,
            'interval_sec': 120,
            'packets_per_capture': 100,
            'total_duration_sec': 300,
            'next_run_ts': None,
            'last_cycle_result': None,
            'total_cycles': 0,
            'start_time': None,
            'end_time': None,
        }

    # CSS: scroll independiente por columna y animaciones
    st.markdown(f"""
        <style>
        /* ══════ HEADER COMPACTO (título + PDF) ══════ */
        [data-testid="stMain"] h1 {{
            padding-top: 0.3rem !important;
            margin-top: 0 !important;
            margin-bottom: 0.2rem !important;
            font-size: 1.6rem !important;
        }}

        /* ══════ SCROLL INDEPENDIENTE POR COLUMNA ══════ */
        /* Bloque principal de 2 columnas: altura fija */
        section[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stHorizontalBlock"] [data-testid="column"]) {{
            max-height: 100vh;
        }}

        /* Cada columna del dashboard: scroll propio */
        section[data-testid="stMain"] [data-testid="column"] {{
            height: calc(100vh - 80px) !important;
            max-height: calc(100vh - 80px) !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }}

        /* Scrollbar personalizado */
        section[data-testid="stMain"] [data-testid="column"]::-webkit-scrollbar {{
            width: 8px;
        }}
        section[data-testid="stMain"] [data-testid="column"]::-webkit-scrollbar-track {{
            background: {c.background};
            border-radius: 10px;
        }}
        section[data-testid="stMain"] [data-testid="column"]::-webkit-scrollbar-thumb {{
            background: {c.surface};
            border-radius: 10px;
            border: 2px solid {c.border};
        }}
        section[data-testid="stMain"] [data-testid="column"]::-webkit-scrollbar-thumb:hover {{
            background: {c.primary};
        }}

        /* Animaciones suaves */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        [data-testid="stMarkdownContainer"] {{
            animation: fadeIn 0.5s ease-out;
        }}
        .gradient-card {{ animation: fadeIn 0.6s ease-out; }}
        .pulse-animation {{ animation: pulse 2s ease-in-out infinite; }}
        </style>
    """, unsafe_allow_html=True)

    # Columnas principales del dashboard
    col1, col2 = st.columns([1, 2], gap="medium")

    # Columna derecha: bienvenida, captura en vivo, o resumen tras predicción
    with col2:
        # Mostrar panel de captura en vivo si está capturando
        if st.session_state.auto_capture.get('is_capturing', False):
            st.markdown("## 🔴 CAPTURA EN VIVO")
            
            # Panel de estadísticas en tiempo real (ligero)
            st.markdown("### 📊 Estadísticas en Tiempo Real")
            
            # Información del ciclo actual
            current_cycle = st.session_state.auto_capture.get('total_cycles', 0) + 1
            st.info(f"📍 **Ciclo #{current_cycle}** en progreso...")
            
            # Estadísticas básicas (simuladas durante captura)
            col_stat1, col_stat2, col_stat3 = st.columns(3, gap="small")
            with col_stat1:
                st.metric("⏱️ Capturando", "~30 seg", help="Duración de captura individual")
            with col_stat2:
                st.metric("📦 Protocolo", "TCP/UDP/ICMP", help="Protocolos en captura")
            with col_stat3:
                st.metric("🎯 Estado", "Activo", delta="Procesando", help="Estado actual")
            
            # Indicador visual de progreso
            st.markdown("### 🔄 Proceso de Captura")
            st.progress(0.5, text="🌐 Capturando paquetes de red...")
            
            # Información adicional
            st.markdown(f"""
            <div style="padding: 20px; background: linear-gradient(135deg, {c.success_light} 0%, {c.surface_overlay} 100%); border-radius: 14px; color: {c.text_primary}; text-align: center; border: 1px solid {c.border}; box-shadow: 0 4px 20px {c.success_light};">
                <h3 style="margin: 0; color: {c.success};">⚡ Captura Activa</h3>
                <p style="margin: 10px 0 0 0; color: {c.text_secondary};">Los resultados aparecerán automáticamente al finalizar</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("💡 **Tip:** Espera unos segundos mientras se captura el tráfico de red. Los resultados se mostrarán automáticamente con gráficas completas.")
            
        # Mostrar resultados si hay predicción completada
        elif 'prediccion_realizada' in st.session_state and st.session_state['prediccion_realizada']:
            st.markdown("## 📄 Resumen de la Predicción")
            resumen = st.session_state['resumen_prediccion']
            st.success(resumen['texto'])
            
            # Gráficas: Pie y Barras
            col_graf1, col_graf2 = st.columns(2, gap="medium")
            with col_graf1:
                pie_fig = px.pie(
                    names=resumen['labels'],
                    values=resumen['values'],
                    color=resumen['labels'],
                    color_discrete_map={
                        'Normal': c.success,
                        'Anómalo': c.error,
                        'DDOS_TCP': c.error,
                        'DDOS_UDP': c.warning,
                        'Reconnaissance': c.primary
                    },
                    title="Distribución porcentual"
                )
                pie_fig.update_traces(textinfo='percent+label')
                st.plotly_chart(pie_fig, use_container_width=True)
            
            with col_graf2:
                # Gráfica de barras
                bar_colors = [(c.success if (str(lbl).lower() == 'normal') else c.error) for lbl in resumen['labels']]
                fig_bar = go.Figure(data=[go.Bar(x=resumen['labels'], y=resumen['values'], text=resumen['values'], textposition='auto', marker_color=bar_colors)])
                fig_bar.update_layout(title='Distribución de Detecciones', title_x=0.5)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Explicación inteligente de la distribución
            with st.expander("🧠 Análisis Inteligente de Resultados", expanded=True):
                model_used = st.session_state.get('model_option_used', 'IForest')
                explicacion_dist = explicar_distribucion(resumen['labels'], resumen['values'], model_used)
                st.markdown(explicacion_dist)
            
            # Resumen ejecutivo general
            with st.expander("📋 Resumen Ejecutivo Completo"):
                if 'metricas_rendimiento' in st.session_state:
                    tiene_patron = 'data_prediccion' in st.session_state and st.session_state['data_prediccion'] is not None
                    resumen_general = generar_resumen_general(
                        resumen, 
                        st.session_state['metricas_rendimiento'],
                        model_used,
                        tiene_patron
                    )
                    st.markdown(resumen_general)
            
            # Diagnóstico OCSVM
            if st.session_state.get('model_option_used') == 'OCSVM' and 'scores' in st.session_state:
                scores = st.session_state['scores']
                if isinstance(scores, (np.ndarray, list)) and len(scores) > 0:
                    try:
                        thr = None
                        if not st.session_state.get('ocsvm_use_sign', True):
                            pct = float(st.session_state.get('ocsvm_percentile', 0.45))
                            thr = np.percentile(scores, 100 * pct)
                        hist_fig = go.Figure()
                        hist_fig.add_trace(go.Histogram(x=scores, nbinsx=30, marker_color=c.primary, name='decision_function'))
                        if thr is not None:
                            hist_fig.add_shape(type='line', x0=thr, x1=thr, y0=0, y1=1, xref='x', yref='paper', line=dict(color=c.error, width=2))
                            hist_fig.add_annotation(x=thr, y=1, yref='paper', text=f"Umbral={thr:.3f}", showarrow=True, arrowhead=1)
                        hist_fig.update_layout(title='OCSVM: distribución de decision_function', title_x=0.5)
                        st.plotly_chart(hist_fig, use_container_width=True)
                    except Exception:
                        pass
            
            # Métricas Internas
            if st.session_state.get('metric_option_used') == 'Internas' and 'y_pred' in st.session_state and 'pp3' in st.session_state:
                y_pred = st.session_state['y_pred']
                pp3 = st.session_state['pp3']
                unique_labels = np.unique(y_pred)
                if len(unique_labels) >= 2:
                    silhouette, calinski, davies = metricas.metrica_internas(pp3, y_pred)
                    mostrar_metricas(silhouette, calinski, davies)
                else:
                    st.info("Las métricas internas requieren al menos dos clases en la predicción.")
            
            # Métricas de Rendimiento con gráficos dinámicos
            if 'metricas_rendimiento' in st.session_state:
                st.markdown("### ⚙️ Métricas de Rendimiento del Sistema")
                met = st.session_state['metricas_rendimiento']
                
                # Crear 2 filas de métricas con gauges
                # Primera fila: CPU y Memoria
                col_gauge1, col_gauge2 = st.columns(2, gap="medium")
                
                with col_gauge1:
                    # Gauge de CPU
                    cpu_color = c.success if met['cpu'] < 60 else c.warning if met['cpu'] < 85 else c.error
                    fig_cpu = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=met['cpu'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "🖥️ Uso de CPU", 'font': {'size': 20, 'color': c.text_primary}},
                        number={'suffix': "%", 'font': {'size': 40, 'color': c.text_primary}},
                        delta={'reference': 50, 'increasing': {'color': c.error}, 'decreasing': {'color': c.success}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': c.text_primary},
                            'bar': {'color': cpu_color, 'thickness': 0.75},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': c.text_primary,
                            'steps': [
                                {'range': [0, 60], 'color': 'rgba(0, 200, 83, 0.2)'},
                                {'range': [60, 85], 'color': 'rgba(255, 167, 38, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(255, 82, 82, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': c.text_primary, 'width': 4},
                                'thickness': 0.75,
                                'value': 85
                            }
                        }
                    ))
                    fig_cpu.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': c.text_primary},
                        height=250,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    st.plotly_chart(fig_cpu, use_container_width=True)
                    # Estado textual
                    cpu_status = "✅ Normal" if met['cpu'] < 60 else "⚠️ Alto" if met['cpu'] < 85 else "🔥 Crítico"
                    st.markdown(f"<div style='text-align: center; font-size: 16px;'><b>Estado:</b> {cpu_status}</div>", unsafe_allow_html=True)
                
                with col_gauge2:
                    # Gauge de Memoria
                    mem_color = c.success if met['memoria'] < 70 else c.warning if met['memoria'] < 85 else c.error
                    fig_mem = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=met['memoria'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "💾 Uso de Memoria RAM", 'font': {'size': 20, 'color': c.text_primary}},
                        number={'suffix': "%", 'font': {'size': 40, 'color': c.text_primary}},
                        delta={'reference': 50, 'increasing': {'color': c.error}, 'decreasing': {'color': c.success}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': c.text_primary},
                            'bar': {'color': mem_color, 'thickness': 0.75},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': c.text_primary,
                            'steps': [
                                {'range': [0, 70], 'color': 'rgba(16, 185, 129, 0.2)'},
                                {'range': [70, 85], 'color': 'rgba(245, 158, 11, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': c.text_primary, 'width': 4},
                                'thickness': 0.75,
                                'value': 85
                            }
                        }
                    ))
                    fig_mem.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': c.text_primary},
                        height=250,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    st.plotly_chart(fig_mem, use_container_width=True)
                    # Estado textual
                    mem_status = "✅ Normal" if met['memoria'] < 70 else "⚠️ Alto" if met['memoria'] < 85 else "🚨 Crítico"
                    st.markdown(f"<div style='text-align: center; font-size: 16px;'><b>Estado:</b> {mem_status}</div>", unsafe_allow_html=True)
                
                # Segunda fila: Disco y Tiempo
                col_gauge3, col_gauge4 = st.columns(2, gap="medium")
                
                with col_gauge3:
                    # Gauge de Disco
                    disk_color = c.success if met['disco'] < 70 else c.warning if met['disco'] < 85 else c.error
                    fig_disk = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=met['disco'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "📀 Uso de Disco", 'font': {'size': 20, 'color': c.text_primary}},
                        number={'suffix': "%", 'font': {'size': 40, 'color': c.text_primary}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': c.text_primary},
                            'bar': {'color': disk_color, 'thickness': 0.75},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': c.text_primary,
                            'steps': [
                                {'range': [0, 70], 'color': 'rgba(16, 185, 129, 0.2)'},
                                {'range': [70, 85], 'color': 'rgba(245, 158, 11, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': c.text_primary, 'width': 4},
                                'thickness': 0.75,
                                'value': 85
                            }
                        }
                    ))
                    fig_disk.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': c.text_primary},
                        height=250,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    st.plotly_chart(fig_disk, use_container_width=True)
                    # Estado textual
                    disk_status = "✅ Espacio OK" if met['disco'] < 70 else "⚠️ Considerar limpieza" if met['disco'] < 85 else "🚨 Casi lleno"
                    st.markdown(f"<div style='text-align: center; font-size: 16px;'><b>Estado:</b> {disk_status}</div>", unsafe_allow_html=True)
                
                with col_gauge4:
                    # Indicador de Tiempo (diferente estilo - más simple)
                    tiempo_color = c.success if met['tiempo'] < 5 else c.warning if met['tiempo'] < 15 else c.error
                    # Calcular un porcentaje relativo (máximo esperado: 30 segundos)
                    tiempo_pct = min((met['tiempo'] / 30) * 100, 100)
                    
                    fig_time = go.Figure(go.Indicator(
                        mode="number+gauge",
                        value=met['tiempo'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "⏱️ Tiempo de Análisis", 'font': {'size': 20, 'color': c.text_primary}},
                        number={'suffix': " seg", 'font': {'size': 40, 'color': c.text_primary}},
                        gauge={
                            'axis': {'range': [None, 30], 'tickwidth': 1, 'tickcolor': c.text_primary},
                            'bar': {'color': tiempo_color, 'thickness': 0.75},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': c.text_primary,
                            'steps': [
                                {'range': [0, 5], 'color': 'rgba(0, 200, 83, 0.2)'},
                                {'range': [5, 15], 'color': 'rgba(255, 167, 38, 0.2)'},
                                {'range': [15, 30], 'color': 'rgba(255, 82, 82, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': c.text_primary, 'width': 4},
                                'thickness': 0.75,
                                'value': 15
                            }
                        }
                    ))
                    fig_time.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': c.text_primary},
                        height=250,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    st.plotly_chart(fig_time, use_container_width=True)
                    # Estado textual
                    time_status = "⚡ Excelente" if met['tiempo'] < 5 else "✅ Bueno" if met['tiempo'] < 15 else "🐌 Lento"
                    st.markdown(f"<div style='text-align: center; font-size: 16px;'><b>Velocidad:</b> {time_status}</div>", unsafe_allow_html=True)
                
                # Explicación inteligente de métricas de rendimiento
                with st.expander("🔍 Interpretación Detallada de Métricas"):
                    explicacion_metricas = explicar_metricas_rendimiento(
                        met['tiempo'], met['cpu'], met['memoria'], met['disco']
                    )
                    st.markdown(explicacion_metricas)
            
            # Gráfica de Patrón de Tráfico y Anomalías
            # Usar datos de la predicción si existen, sino usar datos cargados
            datos_para_grafica = None
            if 'data_prediccion' in st.session_state and st.session_state['data_prediccion'] is not None:
                datos_para_grafica = st.session_state['data_prediccion']
            elif 'data' in st.session_state and st.session_state.data is not None:
                datos_para_grafica = st.session_state.data
            
            if datos_para_grafica is not None and len(datos_para_grafica) > 0:
                st.markdown("### 📈 Patrón de Tráfico y Anomalías")
                
                # Explicación del patrón ANTES de la gráfica
                explicacion_patron = explicar_patron_trafico(datos_para_grafica)
                if explicacion_patron:
                    with st.expander("📊 ¿Qué significa esta gráfica?", expanded=True):
                        st.markdown(explicacion_patron)
                
                try:
                    # Seleccionar solo columnas numéricas para calcular el patrón de tráfico
                    numeric_data = datos_para_grafica.select_dtypes(include=[np.number])
                    
                    if numeric_data.empty or len(numeric_data.columns) == 0:
                        st.warning("⚠️ No hay datos numéricos para visualizar el patrón de tráfico")
                    else:
                        # Calculate traffic metrics
                        traffic_data = numeric_data.mean(axis=1)
                        
                        # Calculate ceiling and floor
                        window = min(20, len(traffic_data) // 2) if len(traffic_data) > 1 else 1
                        ceiling = traffic_data.rolling(window=window, min_periods=1).max()
                        floor = traffic_data.rolling(window=window, min_periods=1).min()
                        
                        # Create traffic pattern figure
                        fig_traffic = go.Figure()

                        # Add main traffic line
                        fig_traffic.add_trace(go.Scatter(
                            x=list(range(len(traffic_data))),
                            y=traffic_data,
                            mode='lines',
                            name='Tráfico',
                            line=dict(color=c.primary, width=1)
                        ))

                        # Add ceiling line
                        fig_traffic.add_trace(go.Scatter(
                            x=list(range(len(ceiling))),
                            y=ceiling,
                            mode='lines',
                            name='Techo',
                            line=dict(color=c.success, width=2, dash='dash')
                        ))

                        # Add floor line
                        fig_traffic.add_trace(go.Scatter(
                            x=list(range(len(floor))),
                            y=floor,
                            mode='lines',
                            name='Suelo',
                            line=dict(color=c.warning, width=2, dash='dash')
                        ))

                        # Update layout
                        fig_traffic.update_layout(
                            title="Patrón de Tráfico y Detección de Anomalías",
                            title_x=0.5,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color=c.text_primary),
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
                                linecolor=c.border
                            ),
                            yaxis=dict(
                                title="Intensidad de Tráfico",
                                showgrid=True,
                                gridcolor=c.surface_overlay,
                                zeroline=False
                            )
                        )

                        st.plotly_chart(fig_traffic, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error al generar visualización de tráfico: {str(e)}")
            
            # Tabla de paquetes capturados (siempre visible debajo de la gráfica de tráfico)
            if 'data_prediccion' in st.session_state and st.session_state['data_prediccion'] is not None:
                st.markdown("### 📊 Paquetes Capturados")
                st.dataframe(st.session_state['data_prediccion'], use_container_width=True)
        
        # Mostrar tabla de paquetes capturados (captura manual completada, aún sin predicción)
        elif st.session_state.get('captura_manual_lista', False):
            st.markdown("### 📊 Paquetes Capturados")
            # Mensaje temporal "Datos listos" (3s)
            msg_listos = st.empty()
            msg_listos.success("✅ Datos capturados listos para predicción")
            if 'data' in st.session_state and st.session_state.data is not None:
                # Mensaje temporal con conteo (6s)
                msg_info = st.empty()
                msg_info.info(f"📏 **{len(st.session_state.data)}** paquetes capturados · Presiona **Realizar Predicción** en el panel izquierdo para analizar.")
                st.dataframe(st.session_state.data, use_container_width=True)
                time.sleep(3)
                msg_listos.empty()
                time.sleep(3)
                msg_info.empty()
            else:
                st.warning("⚠️ No hay datos disponibles")
        
        # Mostrar mensaje de bienvenida si no hay captura ni predicción
        else:
            st.markdown("### 🚀 Comenzar")
            st.info("""
            **Pasos para usar el sistema:**
            
            1. 📌 Selecciona un **modelo de detección** (IForest, OCSVM, KMEANS, AUTOENCODER)
            2. 📊 Elige el tipo de **métrica** (Externas o Internas)
            3. 🎯 Escoge tu método de captura:
               - **🚀 Automática**: Capturas programadas en intervalos
               - **🖐️ Manual**: Captura única bajo demanda
               - **📂 CSV**: Carga un archivo de datos
            4. 🔍 Presiona **"Realizar Predicción"** para analizar
            
            Los resultados aparecerán aquí con gráficas interactivas y análisis detallado.
            """)
    
    # Interfaz Usuario Panel de Control
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

        # Pestañas: Captura Automática, Captura Manual y Cargar CSV
        tab_auto, tab_manual, tab_csv = st.tabs(["🚀 Captura automática", "🖐️ Captura manual", "📂 Cargar archivo CSV"])

        # ---------------- Captura automática (en pestaña) ----------------
        with tab_auto:
            st.title("⚙️ Captura automática")
            
            # Configuración de parámetros
            col_auto_a, col_auto_b = st.columns(2, gap="medium")
            with col_auto_a:
                _default_total_min = max(1, int(st.session_state.auto_capture['total_duration_sec'] // 60))
                _val_total_min = st.number_input(
                    '⏱️ Duración total de la sesión (minutos)', 
                    min_value=1, max_value=1440, value=_default_total_min, step=1,
                    help='⏱️ Tiempo TOTAL que durará toda la sesión de captura automática',
                    disabled=st.session_state.auto_capture['active']
                )
                st.session_state.auto_capture['total_duration_sec'] = int(_val_total_min * 60)
            with col_auto_b:
                _default_interval_min = max(1, int(st.session_state.auto_capture['interval_sec'] // 60))
                _val_interval_min = st.number_input(
                    '🔄 Intervalo entre capturas (minutos)', 
                    min_value=1, max_value=1440, value=_default_interval_min, step=1,
                    help='🔄 Cada cuántos minutos se realizará UNA captura',
                    disabled=st.session_state.auto_capture['active']
                )
                st.session_state.auto_capture['interval_sec'] = int(_val_interval_min * 60)

            # Calcular ciclos esperados
            if st.session_state.auto_capture['active']:
                expected_cycles = int(st.session_state.auto_capture['total_duration_sec'] / st.session_state.auto_capture['interval_sec'])
            else:
                expected_cycles = int(_val_total_min * 60 / (_val_interval_min * 60))
            
            # Mostrar información de la configuración
            if not st.session_state.auto_capture['active']:
                st.info(f"📊 **Configuración:** La sesión durará **{_val_total_min} minuto(s)** con capturas cada **{_val_interval_min} minuto(s)**. Se realizarán aproximadamente **{expected_cycles} capturas** en total.")

            # Estado y métricas de la sesión
            col_status_a, col_status_b, col_status_c = st.columns(3, gap="small")
            with col_status_a:
                auto_status = '🟢 Activa' if st.session_state.auto_capture['active'] else '🔴 Detenida'
                st.metric('Estado', auto_status)
            with col_status_b:
                cycles = st.session_state.auto_capture.get('total_cycles', 0)
                st.metric('Ciclos completados', f"{cycles} / {expected_cycles}")
            with col_status_c:
                if st.session_state.auto_capture['active']:
                    elapsed = int(time.time() - st.session_state.auto_capture['start_time'])
                    # Tiempo restante hasta completar la duración total
                    remaining_total = max(0, st.session_state.auto_capture['total_duration_sec'] - elapsed)
                    hours, remainder = divmod(remaining_total, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    st.metric('⏱️ Sesión termina en', f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Botones de control
            col_btn_a, col_btn_b = st.columns(2, gap="small")
            with col_btn_a:
                if st.button('▶️ Iniciar automática', use_container_width=True, disabled=st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['active'] = True
                    st.session_state.auto_capture['stop_requested'] = False
                    st.session_state.auto_capture['total_cycles'] = 0
                    st.session_state.auto_capture['start_time'] = time.time()
                    st.session_state.auto_capture['end_time'] = time.time() + st.session_state.auto_capture['total_duration_sec']
                    # Ejecutar inmediatamente la primera captura
                    st.session_state.auto_capture['next_run_ts'] = time.time()
                    st.rerun()
            with col_btn_b:
                if st.button('⏹️ Detener automática', use_container_width=True, disabled=not st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['stop_requested'] = True
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['is_capturing'] = False
                    st.session_state.auto_capture['next_run_ts'] = None
                    st.session_state.auto_capture['end_time'] = None
                    st.rerun()

            # Visualización del estado actual con barra de progreso mejorada
            if st.session_state.auto_capture['active']:
                # Verificar si ya se completó el tiempo total
                if st.session_state.auto_capture['end_time'] and time.time() >= st.session_state.auto_capture['end_time']:
                    st.success(f"🎉 **Sesión completada!** Se realizaron {st.session_state.auto_capture['total_cycles']} capturas en total.")
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['is_capturing'] = False
                    st.session_state.auto_capture['next_run_ts'] = None
                    st.balloons()
                elif st.session_state.auto_capture['is_capturing']:
                    # Mostrar spinner animado durante captura
                    st.info('🔄 **Capturando paquetes de red... por favor espera.**')
                elif not st.session_state.auto_capture['is_capturing']:
                    if st.session_state.auto_capture['next_run_ts'] is not None:
                        remaining = max(0, int(st.session_state.auto_capture['next_run_ts'] - time.time()))
                        if remaining > 0:
                            # Calcular progreso para la barra
                            total_interval = st.session_state.auto_capture['interval_sec']
                            progress_pct = 1.0 - (remaining / total_interval)
                            
                            # Convertir tiempo a formato legible
                            m, s = divmod(remaining, 60)
                            
                            # Barra de progreso animada
                            st.progress(progress_pct, text=f"⏳ Próxima captura en: **{m:02d}:{s:02d}** (min:seg)")
                        else:
                            # Momento justo antes de iniciar captura
                            st.progress(1.0, text="🚀 Iniciando captura...")
        
        
        # Comando y utilidades de captura desde backend.capture_utils
        comm_arg = build_tshark_command()
        
        # Función para guardar los paquetes en CSV
        def save_packet_csv(df, path):
            df.to_csv(path, index=False)
            st.success(f"✅ Archivo guardado en {path}")
            
        # Auxiliar: ejecutar predicción y mostrar resultado (manual/automática)
        def run_prediction_on_data(data_df):
            try:
                if data_df is None or len(data_df) == 0:
                    st.error('❌ No se capturaron paquetes. Verifica que haya tráfico de red.')
                    return
                
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

                lista = ['ip_ttl','tos','ip_flags_rb','ip_flags_df','ip_flags_mf']
                if set(lista).issubset(set(data_df.columns)):
                    data_df[lista] = data_df[lista].astype('str')
                    data_df.ip_ttl = data_df.ip_ttl.str.replace(',','.')
                    data_df.tos = data_df.tos.str.replace(',','.')
                    data_df.ip_flags_rb = data_df.ip_flags_rb.str.replace(',','.')
                    data_df.ip_flags_df = data_df.ip_flags_df.str.replace(',','.')
                    data_df.ip_flags_mf = data_df.ip_flags_mf.str.replace(',','.')
                
                # Limpiar valores vacíos y NaN
                data_df = data_df.replace('', np.nan).fillna(0)
                
                # Convertir todas las columnas numéricas a float, reemplazando errores con 0
                for col in data_df.columns:
                    try:
                        data_df[col] = pd.to_numeric(data_df[col], errors='coerce').fillna(0)
                    except:
                        pass

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
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                elif model_option=='AUTOENCODER':
                    normal_count = int(np.count_nonzero(y_pred == 0))
                    ddos_tcp_count = int(np.count_nonzero(y_pred == 1))
                    reconnaissance_count = int(np.count_nonzero(y_pred == 2))
                    ddos_udp_count = int(np.count_nonzero(y_pred == 3))
                    total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                    labels = ['Normal','DDOS_TCP','DDOS_UDP','Reconnaissance']
                    values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                else:
                    n_normales = int((y_pred == 0).sum())
                    n_anomalos = int((y_pred == 1).sum())
                    total = n_normales + n_anomalos
                    labels = ['Normal','Anómalo']
                    values = [n_normales, n_anomalos]
                    resumen_text = f"Se analizaron {total} paquetes. Normales: {n_normales}, Anómalos: {n_anomalos}."

                # Guardar estado completo para el panel derecho (col2)
                tiempo_total = time.time() - start_time
                st.session_state['prediccion_realizada'] = True
                st.session_state['captura_manual_lista'] = False  # Limpiar flag de captura manual
                st.session_state['resumen_prediccion'] = {'texto': resumen_text, 'labels': labels, 'values': values}
                st.session_state['data_prediccion'] = data_df
                st.session_state['y_pred'] = y_pred
                st.session_state['scores'] = scores
                st.session_state['pp3'] = pp3
                st.session_state['model_option_used'] = model_option
                st.session_state['metric_option_used'] = metric_option
                st.session_state['metricas_rendimiento'] = {
                    'tiempo': tiempo_total,
                    'cpu': cpu_usage,
                    'memoria': mem_usage,
                    'disco': disco2[3]
                }

                st.success("✅ Predicción completada. Revisa los resultados en el panel de la derecha →")
                st.rerun()  # Refrescar para mostrar resultados en col2

            except Exception as e:
                st.error(f"❌ Error en la predicción: {str(e)}")

        # ============ EJECUCIÓN AUTOMÁTICA (fuera de tabs, se ejecuta siempre) ============
        # FASE 2: Ejecutar captura si is_capturing está activo
        if st.session_state.auto_capture['active'] and st.session_state.auto_capture['is_capturing']:
            current_cycle = st.session_state.auto_capture.get('total_cycles', 0) + 1
            
            captured_data = None
            duration_sec = 30
            
            use_api = is_streamlit_cloud()
            
            if use_api:
                backend_url = get_backend_url()
                captured_data = capture_via_api(duration_sec, backend_url)
            else:
                auto_comm_arg = build_tshark_command()
                captured_data = capture_local(duration_sec, auto_comm_arg)
            
            # Actualizar contador de ciclos
            st.session_state.auto_capture['total_cycles'] = current_cycle
            st.session_state.auto_capture['is_capturing'] = False
            
            if captured_data is not None and len(captured_data) > 0:
                st.session_state.data = captured_data
                
                # Programar siguiente ciclo o finalizar
                time_remaining = st.session_state.auto_capture['end_time'] - time.time()
                if time_remaining < st.session_state.auto_capture['interval_sec']:
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['next_run_ts'] = None
                else:
                    st.session_state.auto_capture['next_run_ts'] = time.time() + st.session_state.auto_capture['interval_sec']
                
                # Ejecutar predicción (esto hace st.rerun() al final si tiene éxito)
                run_prediction_on_data(captured_data)
            else:
                # No se capturaron datos, programar siguiente ciclo
                st.warning("⚠️ No se capturaron paquetes en este ciclo.")
                time_remaining = st.session_state.auto_capture['end_time'] - time.time()
                if time_remaining < st.session_state.auto_capture['interval_sec']:
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['next_run_ts'] = None
                else:
                    st.session_state.auto_capture['next_run_ts'] = time.time() + st.session_state.auto_capture['interval_sec']
                st.rerun()
        
        # FASE 1: Programar captura si es momento (due)
        elif st.session_state.auto_capture['active'] and not st.session_state.auto_capture['is_capturing']:
            # Verificar si se acabó el tiempo total
            if st.session_state.auto_capture['end_time'] and time.time() >= st.session_state.auto_capture['end_time']:
                pass  # La UI en tab_auto maneja el mensaje de completado
            else:
                due = st.session_state.auto_capture['next_run_ts'] is not None and time.time() >= st.session_state.auto_capture['next_run_ts']
                if due:
                    # Activar captura y hacer rerun para que col2 muestre panel en vivo
                    st.session_state.auto_capture['is_capturing'] = True
                    st.rerun()

        # Streamlit UI (contenido de pestañas)
        data = None  # Inicializamos el DataFrame

        # ---------------- Pestaña: Captura manual ----------------
        with tab_manual:
            st.title("🖐️ Captura manual")

            # Parámetros manuales
            col_man_a, col_man_b = st.columns(2, gap="medium")
            with col_man_a:
                manual_packets = st.number_input('Paquetes a capturar (manual)', min_value=10, max_value=50000, value=100, step=10)
            with col_man_b:
                manual_duration_min = st.number_input('Duración máx. (min) (manual)', min_value=1, max_value=1440, value=1, step=1)
            manual_duration = int(manual_duration_min * 60)

            # Botones de acción: misma fila, mismo ancho que los inputs
            col_btn_cap, col_btn_save = st.columns(2, gap="medium")
            with col_btn_cap:
                btn_capture = st.button("🚀 Iniciar Captura", key="btn_manual_capture", use_container_width=True, type="primary")
            with col_btn_save:
                # Botón de guardar CSV (solo habilitado si hay datos capturados)
                has_manual_data = 'data' in st.session_state and st.session_state.data is not None
                if has_manual_data:
                    if st.button("💾 Guardar en CSV", key="btn_save_csv", use_container_width=True):
                        save_packet_csv(st.session_state.data, "captura_paquetes.csv")
                else:
                    st.button("💾 Guardar en CSV", key="btn_save_csv_disabled", use_container_width=True, disabled=True,
                              help="Primero captura paquetes para poder guardarlos")

            if btn_capture:
                # Detectar si estamos en Cloud o local
                use_api = is_streamlit_cloud()
                
                if use_api:
                    # Usar backend API (Streamlit Cloud)
                    st.info("🌐 Capturando desde backend remoto...")
                    backend_url = get_backend_url()
                    progress_bar = st.progress(0, text="⏳ Esperando respuesta del backend...")
                    
                    captured_data = capture_via_api(manual_duration, backend_url)
                    progress_bar.empty()
                    
                    if captured_data is not None and len(captured_data) > 0:
                        st.success(f"✅ Captura finalizada: {len(captured_data)} paquetes capturados")
                    else:
                        st.warning("⚠️ No se capturaron paquetes")
                else:
                    # Usar tshark local
                    info_placeholder = st.empty()
                    info_placeholder.info("💻 Capturando desde interfaz local...")
                    process = capturing_packets(comm_arg)
                    
                    # Inicializamos el DataFrame
                    captured_data = None
                    progress_bar = st.progress(0, text="🌐 Preparando captura de paquetes...")
                    total_packets = manual_packets
                    start_ts = time.time()

                    i = 0
                    while i < total_packets:
                        # Parar por tiempo si está configurado
                        if manual_duration and (time.time() - start_ts) >= manual_duration:
                            break
                        packet_str = process.stdout.readline().strip()
                        if packet_str:
                            packet_list = packet_str.split("\t")
                            type_packet_data = type_packet(packet_list)
                            captured_data = packet_df(type_packet_data, captured_data)
                            i += 1
                            pct = i / total_packets
                            progress_bar.progress(pct, text=f"📡 Capturando paquetes: **{i}/{total_packets}** ({pct*100:.0f}%)")

                    try:
                        process.terminate()
                    except Exception:
                        pass
                    progress_bar.empty()
                    # Desaparece el mensaje de "Capturando desde interfaz local..."
                    info_placeholder.empty()
                    # Mensaje temporal "Captura finalizada" (2.5s)
                    finalizado_placeholder = st.empty()
                    finalizado_placeholder.success("✅ Captura finalizada.")
                    time.sleep(2.5)
                    finalizado_placeholder.empty()

                # Guardar datos capturados y refrescar para mostrar en col2
                if captured_data is not None and len(captured_data) > 0:
                    if not (list(captured_data.columns) == ['value'] and len(captured_data) == 0):
                        st.session_state.data = captured_data
                        st.session_state['captura_manual_lista'] = True
                        st.rerun()
                    else:
                        st.warning("⚠️ No se capturaron paquetes válidos")
                else:
                    st.warning("⚠️ No se capturaron datos")

        # ---------------- Pestaña: Cargar archivo CSV ----------------
        with tab_csv:
            st.title("📂 Cargar archivo CSV")
            st.markdown("### 📊 Cargar Datos para Predicción")
            
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
                        st.success("✅ Datos cargados exitosamente")
                        
                        with st.expander("📊 Vista previa de datos"):
                            st.dataframe(data.head(), use_container_width=True)
                            st.info(f"📏 Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")
                        
                        # Guardar en session_state
                        st.session_state.data = data
                except pd.errors.EmptyDataError:
                    st.error("❌ El archivo CSV está vacío o no tiene columnas válidas.")
                    data = None
                except Exception as e:
                    st.error(f"❌ Error al cargar el archivo: {str(e)}")
                    data = None
            else:
                st.info("⬆️ Selecciona un archivo CSV para cargar los datos")

        # Botón de predicción fuera de las pestañas (común para todas)
        st.markdown("---")
        
        # Determinar qué datos usar para la predicción
        data = None
        if 'data' in st.session_state and st.session_state.data is not None:
            data = st.session_state.data

        if st.button('🚀 Realizar Predicción', key='predict', use_container_width=True):
            if data is not None:
                run_prediction_on_data(data)
            else:
                st.warning("⚠ Por favor capture paquetes o cargue un archivo CSV antes de realizar la predicción.")
        
        # Botón para limpiar y volver a predecir
        if st.session_state.get('prediccion_realizada', False):
            if st.button('🔄 Volver a Predecir', key='reset_prediction', use_container_width=True, type="secondary"):
                # Limpiar todos los estados de predicción
                st.session_state['prediccion_realizada'] = False
                st.session_state['resumen_prediccion'] = None
                st.session_state['data_prediccion'] = None
                st.session_state['y_pred'] = None
                st.session_state['scores'] = None
                st.session_state['pp3'] = None
                st.session_state['model_option_used'] = None
                st.session_state['metric_option_used'] = None
                st.session_state['metricas_rendimiento'] = None
                st.success("✅ Predicción limpiada. Puedes realizar una nueva predicción.")
                st.rerun()

    # ============ AUTO-REFRESH para cuenta regresiva (fuera de col1/col2) ============
    # Si la captura automática está activa y esperando el siguiente ciclo, refrescar cada segundo
    if st.session_state.auto_capture.get('active', False) and not st.session_state.auto_capture.get('is_capturing', False):
        if st.session_state.auto_capture.get('next_run_ts') is not None:
            remaining = st.session_state.auto_capture['next_run_ts'] - time.time()
            if remaining > 0:
                time.sleep(1)
                st.rerun()

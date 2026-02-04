"""
Componente de sidebar con controles del dashboard.
"""

import streamlit as st
from config.settings import AVAILABLE_MODELS, METRIC_TYPES


def render_model_selector() -> str:
    """
    Renderizar selector de modelo.
    
    Returns:
        Modelo seleccionado
    """
    return st.selectbox(
        "📌 Seleccione el modelo de detección",
        AVAILABLE_MODELS,
        help="Cada modelo utiliza diferentes técnicas para detectar anomalías"
    )


def render_metric_selector() -> str:
    """
    Renderizar selector de tipo de métrica.
    
    Returns:
        Tipo de métrica seleccionado
    """
    return st.selectbox(
        "📌 Seleccione el tipo de métrica",
        METRIC_TYPES,
        help="Internas: Silhouette, Calinski, Davies. Externas: requiere etiquetas reales."
    )


def render_manual_capture_controls() -> dict:
    """
    Renderizar controles de captura manual.
    
    Returns:
        Diccionario con configuración {packets, duration_min}
    """
    st.title("🖐️ Captura manual")
    
    col_a, col_b = st.columns(2)
    with col_a:
        packets = st.number_input(
            'Paquetes a capturar (manual)', 
            min_value=10, 
            max_value=50000, 
            value=100, 
            step=10
        )
    with col_b:
        duration_min = st.number_input(
            'Duración máx. (min) (manual)', 
            min_value=0, 
            max_value=1440, 
            value=0, 
            step=1
        )
    
    return {'packets': packets, 'duration_min': duration_min}


def render_auto_capture_controls() -> dict:
    """
    Renderizar controles de captura automática.
    
    Returns:
        Diccionario con configuración
    """
    st.title("⚙️ Captura automática")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if 'auto_capture' not in st.session_state:
            default_dur = 1
        else:
            default_dur = max(1, int(st.session_state.auto_capture.get('duration_sec', 60) // 60))
        
        duration_min = st.number_input(
            'Duración de captura (minutos)', 
            min_value=1, 
            max_value=1440, 
            value=default_dur, 
            step=1,
            help='La captura automática finalizará cuando se cumpla este tiempo'
        )
    
    with col_b:
        if 'auto_capture' not in st.session_state:
            default_interval = 5
        else:
            default_interval = max(1, int(st.session_state.auto_capture.get('interval_sec', 300) // 60))
        
        interval_min = st.number_input(
            'Intervalo entre capturas (minutos)', 
            min_value=1, 
            max_value=1440, 
            value=default_interval, 
            step=1,
            help='Pausa (en minutos) entre el fin de una captura y el inicio de la siguiente'
        )
    
    return {
        'duration_min': duration_min,
        'interval_min': interval_min
    }


def render_auto_capture_buttons() -> tuple:
    """
    Renderizar botones de control de captura automática.
    
    Returns:
        Tuple (start_clicked, stop_clicked)
    """
    col_a, col_b = st.columns(2)
    
    is_active = st.session_state.get('auto_capture', {}).get('active', False)
    
    with col_a:
        start_clicked = st.button(
            '▶️ Iniciar automática', 
            use_container_width=True, 
            disabled=is_active
        )
    
    with col_b:
        stop_clicked = st.button(
            '⏹️ Detener automática', 
            use_container_width=True, 
            disabled=not is_active
        )
    
    return start_clicked, stop_clicked


def initialize_auto_capture_state() -> None:
    """Inicializar estado de captura automática en session_state."""
    if 'auto_capture' not in st.session_state:
        st.session_state.auto_capture = {
            'active': False,
            'is_capturing': False,
            'stop_requested': False,
            'interval_sec': 300,
            'packets_per_capture': 100,
            'duration_sec': 60,
            'next_run_ts': None,
            'last_cycle_result': None,
        }

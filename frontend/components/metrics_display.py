"""
Componentes para mostrar métricas y estadísticas.
"""

import streamlit as st
from typing import Dict, Any
from config.theme import theme
from frontend.utils import format_number, format_percentage, format_duration


def show_resource_metrics(
    tiempo: float,
    cpu: float,
    memoria: float,
    disco: float
) -> None:
    """
    Mostrar métricas de recursos del sistema con diseño mejorado.
    
    Args:
        tiempo: Tiempo de ejecución en segundos
        cpu: Porcentaje de uso de CPU
        memoria: Porcentaje de uso de memoria
        disco: Porcentaje de uso de disco
    """
    # Crear cards con el tema
    st.markdown(
        f"""
        <div style="
            background: {theme.colors.surface_variant};
            padding: {theme.spacing.md};
            border-radius: {theme.radius.lg};
            margin-bottom: {theme.spacing.lg};
            border: 1px solid {theme.colors.border};
        ">
            <h3 style="
                color: {theme.colors.text_primary};
                margin-bottom: {theme.spacing.md};
                font-weight: {theme.typography.weight_semibold};
            ">📊 Recursos del Sistema</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    cols = st.columns(4)
    
    # Determinar colores basados en umbrales
    cpu_delta = f"{cpu:.1f}%" if cpu < 80 else None
    cpu_delta_color = "normal" if cpu < 80 else "inverse"
    
    mem_delta = f"{memoria:.1f}%" if memoria < 80 else None
    mem_delta_color = "normal" if memoria < 80 else "inverse"
    
    with cols[0]:
        st.metric(
            "⏱️ Tiempo",
            format_duration(tiempo),
            help="Tiempo total de ejecución"
        )
    with cols[1]:
        st.metric(
            "🖥️ CPU",
            f"{cpu:.1f}%",
            delta=cpu_delta,
            delta_color=cpu_delta_color,
            help="Uso de procesador"
        )
    with cols[2]:
        st.metric(
            "💾 Memoria",
            f"{memoria:.1f}%",
            delta=mem_delta,
            delta_color=mem_delta_color,
            help="Uso de RAM"
        )
    with cols[3]:
        st.metric(
            "📀 Disco",
            f"{disco:.1f}%",
            help="Uso de almacenamiento"
        )



def show_prediction_summary(
    total: int,
    normal: int,
    anomalous: int = 0,
    ddos_tcp: int = 0,
    ddos_udp: int = 0,
    reconnaissance: int = 0,
    model_type: str = 'binary'
) -> str:
    """
    Generar y mostrar resumen de predicción.
    
    Args:
        total: Total de paquetes analizados
        normal: Cantidad de paquetes normales
        anomalous: Cantidad de paquetes anómalos (para modelos binarios)
        ddos_tcp: Cantidad de ataques DDoS TCP
        ddos_udp: Cantidad de ataques DDoS UDP
        reconnaissance: Cantidad de ataques de reconocimiento
        model_type: Tipo de modelo ('binary' o 'multiclass')
        
    Returns:
        Texto del resumen
    """
    if model_type == 'multiclass':
        resumen_text = (
            f"Se analizaron {total} paquetes. "
            f"Normal: {normal}, "
            f"DDOS_TCP: {ddos_tcp}, "
            f"DDOS_UDP: {ddos_udp}, "
            f"Reconnaissance: {reconnaissance}."
        )
    else:
        resumen_text = (
            f"Se analizaron {total} paquetes. "
            f"Normales: {normal}, "
            f"Anómalos: {anomalous}."
        )
    
    return resumen_text


def show_welcome_message() -> None:
    """Mostrar mensaje de bienvenida en el dashboard."""
    st.markdown("## 👋 Bienvenido al Panel IDS")
    st.info(
        "Aquí verás el resumen y visualización de los resultados una vez "
        "realices una predicción. Selecciona el modelo y las opciones en el "
        "panel de la izquierda, luego captura paquetes y realiza la predicción."
    )


def show_capture_status(
    active: bool,
    next_capture_time: str = None
) -> None:
    """
    Mostrar estado de captura automática.
    
    Args:
        active: Si la captura está activa
        next_capture_time: Tiempo para la próxima captura (formato MM:SS)
    """
    status = '🟢 Activa' if active else '🔴 Detenida'
    st.metric('Estado', status)
    
    if active and next_capture_time:
        st.info(f"⏳ Próxima captura en {next_capture_time}")


def show_dataset_info(rows: int, cols: int) -> None:
    """
    Mostrar información del dataset cargado.
    
    Args:
        rows: Número de filas
        cols: Número de columnas
    """
    st.info(f"Dimensiones del dataset: {rows} filas, {cols} columnas")


def create_metrics_card(
    title: str,
    metrics: Dict[str, Any],
    container_style: str = None
) -> None:
    """
    Crear tarjeta de métricas personalizada.
    
    Args:
        title: Título de la tarjeta
        metrics: Diccionario de métricas {nombre: valor}
        container_style: Estilos CSS opcionales
    """
    with st.container():
        st.markdown(f"### {title}")
        cols = st.columns(len(metrics))
        for idx, (key, value) in enumerate(metrics.items()):
            with cols[idx]:
                if isinstance(value, float):
                    st.metric(key, f"{value:.4f}")
                else:
                    st.metric(key, value)

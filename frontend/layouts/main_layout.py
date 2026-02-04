"""
Layouts principales para la aplicación.
"""

import streamlit as st
from config.theme import theme


def create_main_layout(page_title: str, show_sidebar: bool = True):
    """
    Crear layout principal con header y estilos consistentes.
    
    Args:
        page_title: Título de la página
        show_sidebar: Si mostrar el sidebar
    """
    if show_sidebar:
        with st.sidebar:
            render_sidebar_header()
    
    create_page_header(page_title)


def render_sidebar_header():
    """Renderizar header del sidebar."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {theme.colors.primary} 0%, {theme.colors.secondary} 100%);
            padding: {theme.spacing.lg};
            border-radius: {theme.radius.lg};
            text-align: center;
            margin-bottom: {theme.spacing.xl};
        ">
            <h2 style="color: white; margin: 0;">🛡️ Sistema IDS</h2>
            <p style="color: white; margin: 0; opacity: 0.9; font-size: {theme.typography.size_sm};">
                Detección de Intrusiones IoT
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def create_page_header(title: str, subtitle: str = None, icon: str = "🛡️"):
    """
    Crear header consistente para cada página.
    
    Args:
        title: Título principal
        subtitle: Subtítulo opcional
        icon: Emoji/icono
    """
    subtitle_html = f"<p style='color: white; opacity: 0.9; margin-top: {theme.spacing.sm}; font-size: {theme.typography.size_base};'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(
        f"""
        <div class="main-header">
            <h1 style="margin: 0; font-size: {theme.typography.size_3xl}; font-weight: {theme.typography.weight_bold};">
                {icon} {title}
            </h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def create_info_card(title: str, content: str, variant: str = "info"):
    """
    Crear card informativa con estilos del tema.
    
    Args:
        title: Título del card
        content: Contenido del card
        variant: Tipo de card (info, success, warning, error)
    """
    color_map = {
        "info": theme.colors.info,
        "success": theme.colors.success,
        "warning": theme.colors.warning,
        "error": theme.colors.error,
    }
    
    border_color = color_map.get(variant, theme.colors.info)
    
    st.markdown(
        f"""
        <div style="
            background: {theme.colors.surface_variant};
            border-left: 4px solid {border_color};
            padding: {theme.spacing.lg};
            border-radius: {theme.radius.md};
            margin: {theme.spacing.md} 0;
            box-shadow: {theme.shadows.sm};
        ">
            <h3 style="
                margin: 0 0 {theme.spacing.sm} 0;
                color: {theme.colors.text_primary};
                font-size: {theme.typography.size_lg};
                font-weight: {theme.typography.weight_semibold};
            ">{title}</h3>
            <p style="
                margin: 0;
                color: {theme.colors.text_secondary};
                font-size: {theme.typography.size_base};
            ">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def create_metric_container(metrics: list[dict]):
    """
    Crear contenedor de métricas con grid responsive.
    
    Args:
        metrics: Lista de diccionarios con keys 'label', 'value', 'delta'
    """
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            st.metric(
                label=metric.get('label'),
                value=metric.get('value'),
                delta=metric.get('delta')
            )


def create_two_column_layout(left_content_fn, right_content_fn, ratio: list = [1, 1]):
    """
    Crear layout de dos columnas.
    
    Args:
        left_content_fn: Función que renderiza contenido izquierdo
        right_content_fn: Función que renderiza contenido derecho
        ratio: Proporción de las columnas [left, right]
    """
    left_col, right_col = st.columns(ratio)
    
    with left_col:
        left_content_fn()
    
    with right_col:
        right_content_fn()


def create_card_grid(items: list[dict], columns: int = 3):
    """
    Crear grid de cards.
    
    Args:
        items: Lista de diccionarios con keys 'title', 'content', 'icon'
        columns: Número de columnas
    """
    cols = st.columns(columns)
    
    for idx, item in enumerate(items):
        col_idx = idx % columns
        with cols[col_idx]:
            icon = item.get('icon', '📊')
            title = item.get('title', '')
            content = item.get('content', '')
            
            st.markdown(
                f"""
                <div class="card">
                    <h3 style="margin: 0 0 {theme.spacing.sm} 0;">
                        {icon} {title}
                    </h3>
                    <p style="margin: 0; color: {theme.colors.text_secondary};">
                        {content}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


def create_loading_state(message: str = "Cargando..."):
    """
    Crear estado de carga con spinner.
    
    Args:
        message: Mensaje a mostrar
    """
    return st.spinner(f"⏳ {message}")


def create_empty_state(title: str, message: str, icon: str = "📭"):
    """
    Crear estado vacío cuando no hay datos.
    
    Args:
        title: Título del estado vacío
        message: Mensaje descriptivo
        icon: Icono a mostrar
    """
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: {theme.spacing.xxxl};
            background: {theme.colors.surface_variant};
            border-radius: {theme.radius.lg};
            margin: {theme.spacing.xl} 0;
        ">
            <div style="font-size: 64px; margin-bottom: {theme.spacing.lg};">
                {icon}
            </div>
            <h3 style="
                color: {theme.colors.text_primary};
                margin-bottom: {theme.spacing.md};
                font-weight: {theme.typography.weight_semibold};
            ">{title}</h3>
            <p style="
                color: {theme.colors.text_secondary};
                font-size: {theme.typography.size_base};
            ">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

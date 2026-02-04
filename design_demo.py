"""
Página de ejemplo del sistema de diseño.
Esta página demuestra todos los componentes y estilos del tema.
"""

import streamlit as st
from config.theme import theme
from frontend.layouts import (
    create_page_header,
    create_info_card,
    create_metric_container,
    create_card_grid,
    create_empty_state,
)
from frontend.utils import (
    format_number,
    format_percentage,
    format_bytes,
    format_attack_name,
)


def show_design_system_demo():
    """Mostrar página de demostración del sistema de diseño."""
    
    create_page_header(
        "Sistema de Diseño",
        subtitle="Demostración de componentes y estilos",
        icon="🎨"
    )
    
    # Sección: Colores
    st.markdown("## 🎨 Paleta de Colores")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### Principales")
        _show_color_swatch("Primary", theme.colors.primary)
        _show_color_swatch("Secondary", theme.colors.secondary)
        _show_color_swatch("Accent", theme.colors.accent)
    
    with col2:
        st.markdown("### Estados")
        _show_color_swatch("Success", theme.colors.success)
        _show_color_swatch("Warning", theme.colors.warning)
        _show_color_swatch("Error", theme.colors.error)
        _show_color_swatch("Info", theme.colors.info)
    
    with col3:
        st.markdown("### Ataques")
        _show_color_swatch("Normal", theme.colors.normal)
        _show_color_swatch("Anomaly", theme.colors.anomaly)
        _show_color_swatch("DDoS TCP", theme.colors.ddos_tcp)
        _show_color_swatch("DDoS UDP", theme.colors.ddos_udp)
    
    with col4:
        st.markdown("### Superficies")
        _show_color_swatch("Surface", theme.colors.surface)
        _show_color_swatch("Background", theme.colors.background)
        _show_color_swatch("Border", theme.colors.border)
    
    st.divider()
    
    # Sección: Tipografía
    st.markdown("## 📝 Tipografía")
    
    st.markdown(
        f"""
        <div style="font-family: {theme.typography.font_family};">
            <h1 style="font-size: {theme.typography.size_4xl}; font-weight: {theme.typography.weight_bold};">
                Heading 1 - 4XL Bold
            </h1>
            <h2 style="font-size: {theme.typography.size_3xl}; font-weight: {theme.typography.weight_bold};">
                Heading 2 - 3XL Bold
            </h2>
            <h3 style="font-size: {theme.typography.size_2xl}; font-weight: {theme.typography.weight_semibold};">
                Heading 3 - 2XL Semibold
            </h3>
            <p style="font-size: {theme.typography.size_base}; font-weight: {theme.typography.weight_normal};">
                Texto base - Base Normal
            </p>
            <p style="font-size: {theme.typography.size_sm}; color: {theme.colors.text_secondary};">
                Texto secundario - SM Normal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Sección: Cards Informativos
    st.markdown("## 📋 Cards Informativos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_info_card(
            "Información",
            "Este es un card informativo con el estilo del tema.",
            variant="info"
        )
        create_info_card(
            "Éxito",
            "Operación completada exitosamente.",
            variant="success"
        )
    
    with col2:
        create_info_card(
            "Advertencia",
            "Ten cuidado con esta acción.",
            variant="warning"
        )
        create_info_card(
            "Error",
            "Algo salió mal en el proceso.",
            variant="error"
        )
    
    st.divider()
    
    # Sección: Métricas
    st.markdown("## 📊 Métricas")
    
    metrics = [
        {'label': '📦 Total Paquetes', 'value': format_number(123456), 'delta': '+2.5%'},
        {'label': '✅ Normal', 'value': format_number(120000), 'delta': None},
        {'label': '⚠️ Anomalías', 'value': format_number(3456), 'delta': '-1.2%'},
        {'label': '🎯 Precisión', 'value': format_percentage(0.9734), 'delta': '+0.3%'},
    ]
    
    create_metric_container(metrics)
    
    st.divider()
    
    # Sección: Grid de Cards
    st.markdown("## 🔲 Grid de Cards")
    
    items = [
        {
            'icon': '🛡️',
            'title': 'Detección en Tiempo Real',
            'content': 'Análisis instantáneo de tráfico de red'
        },
        {
            'icon': '🤖',
            'title': 'Machine Learning',
            'content': '4 modelos de ML para detección precisa'
        },
        {
            'icon': '📈',
            'title': 'Visualización',
            'content': 'Gráficos interactivos y reportes PDF'
        },
        {
            'icon': '⚡',
            'title': 'Alto Rendimiento',
            'content': 'Optimizado para Raspberry Pi'
        },
        {
            'icon': '🔒',
            'title': 'Seguridad',
            'content': 'Protección contra múltiples amenazas'
        },
        {
            'icon': '📊',
            'title': 'Métricas',
            'content': 'Análisis detallado del sistema'
        },
    ]
    
    create_card_grid(items, columns=3)
    
    st.divider()
    
    # Sección: Formatters
    st.markdown("## 🔧 Formatters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Números y Porcentajes")
        st.write(f"Número: {format_number(1234567)}")
        st.write(f"Porcentaje: {format_percentage(0.9534)}")
        st.write(f"Bytes: {format_bytes(1536000)}")
    
    with col2:
        st.markdown("### Nombres de Ataque")
        st.write(f"ddos_tcp → {format_attack_name('ddos_tcp')}")
        st.write(f"normal → {format_attack_name('normal')}")
        st.write(f"portscan → {format_attack_name('portscan')}")
    
    st.divider()
    
    # Sección: Estado Vacío
    st.markdown("## 📭 Estado Vacío")
    
    create_empty_state(
        "No hay datos disponibles",
        "Este es un ejemplo de cómo se ve el estado vacío cuando no hay información para mostrar.",
        icon="📭"
    )
    
    st.divider()
    
    # Sección: Botones y Controles
    st.markdown("## 🎛️ Botones y Controles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Botón Primario", use_container_width=True):
            st.success("¡Botón primario presionado!")
    
    with col2:
        if st.button("⚠️ Botón Advertencia", use_container_width=True):
            st.warning("¡Botón de advertencia presionado!")
    
    with col3:
        if st.button("❌ Botón Peligro", use_container_width=True):
            st.error("¡Botón de peligro presionado!")
    
    st.divider()
    
    # Sección: Inputs
    st.markdown("## 📝 Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Campo de texto", placeholder="Escribe algo...")
        st.number_input("Campo numérico", min_value=0, max_value=100, value=50)
    
    with col2:
        st.selectbox("Selector", ["Opción 1", "Opción 2", "Opción 3"])
        st.slider("Slider", min_value=0, max_value=100, value=50)
    
    st.divider()
    
    # Información del tema
    st.markdown("## ℹ️ Información del Tema")
    
    with st.expander("Ver Tokens del Tema"):
        st.json({
            "colors": {
                "primary": theme.colors.primary,
                "secondary": theme.colors.secondary,
                "success": theme.colors.success,
            },
            "typography": {
                "font_family": theme.typography.font_family,
                "size_base": theme.typography.size_base,
            },
            "spacing": {
                "sm": theme.spacing.sm,
                "md": theme.spacing.md,
                "lg": theme.spacing.lg,
            },
            "radius": {
                "sm": theme.radius.sm,
                "md": theme.radius.md,
                "lg": theme.radius.lg,
            }
        })


def _show_color_swatch(name: str, color: str):
    """Mostrar muestra de color."""
    st.markdown(
        f"""
        <div style="
            background: {color};
            padding: {theme.spacing.md};
            border-radius: {theme.radius.md};
            margin-bottom: {theme.spacing.sm};
            text-align: center;
            color: white;
            font-weight: {theme.typography.weight_semibold};
            box-shadow: {theme.shadows.sm};
        ">
            {name}
        </div>
        <div style="
            text-align: center;
            font-size: {theme.typography.size_xs};
            color: {theme.colors.text_secondary};
            font-family: {theme.typography.font_family_mono};
            margin-bottom: {theme.spacing.md};
        ">
            {color}
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    from frontend.style import setup_page_and_style
    setup_page_and_style()
    show_design_system_demo()

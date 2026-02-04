"""
Configuración de estilos y tema de la aplicación.
"""

import streamlit as st
from config.theme import theme


def setup_page_and_style():
    """Configurar página y aplicar estilos del tema."""
    st.set_page_config(
        page_title="Sistema IDS IoT - Detección de Intrusiones",
        page_icon="🛡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Generar CSS usando design tokens
    css = generate_custom_css()
    st.markdown(css, unsafe_allow_html=True)


def generate_custom_css() -> str:
    """Generar CSS personalizado usando el sistema de tema."""
    
    # Obtener tokens del tema
    colors = theme.colors
    typo = theme.typography
    spacing = theme.spacing
    radius = theme.radius
    transitions = theme.transitions
    
    return f"""
<style>
    /* Variables CSS */
    {theme.generate_css()}
    
    /* Estilos globales */
    body {{
        color: {colors.text_primary};
        font-family: {typo.font_family};
        background-color: {colors.background};
    }}
    
    /* Headers */
    .main-header {{
        font-family: {typo.font_family};
        background: linear-gradient(135deg, {colors.primary} 0%, {colors.secondary} 100%);
        padding: {spacing.lg};
        border-radius: {radius.lg};
        color: white;
        text-align: center;
        margin-bottom: {spacing.xl};
        box-shadow: {theme.shadows.md};
    }}
    
    /* Cards mejoradas */
    .metric-card {{
        background: {colors.surface_variant};
        padding: {spacing.lg};
        border-radius: {radius.lg};
        box-shadow: {theme.shadows.md};
        margin: {spacing.md} 0;
        transition: all {transitions.base} {transitions.ease};
        border: 1px solid {colors.border};
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: {theme.shadows.lg};
        border-color: {colors.primary};
    }}
    
    .card {{
        background: {colors.surface_variant};
        padding: {spacing.lg};
        border-radius: {radius.lg};
        box-shadow: {theme.shadows.sm};
        margin-bottom: {spacing.lg};
        border: 1px solid {colors.border};
    }}
    
    /* Botones mejorados */
    .stButton > button {{
        background: {colors.surface_variant};
        border: 1px solid {colors.border};
        color: {colors.text_primary};
        padding: {spacing.sm} {spacing.lg};
        border-radius: {radius.md};
        box-shadow: {theme.shadows.sm};
        transition: all {transitions.base} {transitions.ease};
        font-weight: {typo.weight_medium};
        font-family: {typo.font_family};
    }}
    
    .stButton > button:hover {{
        background: {colors.primary};
        border-color: {colors.primary};
        transform: translateY(-2px);
        box-shadow: {theme.shadows.md};
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: {theme.shadows.sm};
    }}
    
    /* Alerts mejorados */
    .stAlert {{
        background-color: {colors.surface_variant};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {radius.md};
        padding: {spacing.md};
    }}
    
    /* Success alert */
    .stAlert[data-baseweb="notification"][kind="success"] {{
        border-left: 4px solid {colors.success};
    }}
    
    /* Warning alert */
    .stAlert[data-baseweb="notification"][kind="warning"] {{
        border-left: 4px solid {colors.warning};
    }}
    
    /* Error alert */
    .stAlert[data-baseweb="notification"][kind="error"] {{
        border-left: 4px solid {colors.error};
    }}
    
    /* Info alert */
    .stAlert[data-baseweb="notification"][kind="info"] {{
        border-left: 4px solid {colors.info};
    }}
    
    /* Inputs mejorados */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        color: {colors.text_primary} !important;
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
        transition: all {transitions.base} {transitions.ease};
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 2px rgba(75, 159, 225, 0.2) !important;
    }}
    
    /* Select boxes */
    .stSelectbox > div > div {{
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
    }}
    
    /* DataFrames */
    .stDataFrame {{
        color: {colors.text_primary};
        border-radius: {radius.md};
        overflow: hidden;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {colors.surface_variant} !important;
        color: {colors.text_primary} !important;
        border-radius: {radius.md} !important;
        padding: {spacing.md} !important;
    }}
    
    /* Notifications con animación */
    .notification {{
        padding: {spacing.md};
        border-radius: {radius.md};
        margin-bottom: {spacing.md};
        animation: slideIn {transitions.slow} {transitions.ease};
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeOut {{
        from {{ opacity: 1; }}
        to {{ opacity: 0; height: 0; padding: 0; margin: 0; }}
    }}
    
    /* Success animation */
    .success-animation {{
        animation: pulse 1.5s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors.surface};
        border-radius: {radius.md};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors.border};
        border-radius: {radius.md};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors.primary};
    }}
    
    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {{
        background-color: {colors.surface};
        border-right: 1px solid {colors.border};
    }}
    
    /* Metrics mejorados */
    [data-testid="stMetricValue"] {{
        font-size: {typo.size_2xl};
        font-weight: {typo.weight_bold};
        color: {colors.primary};
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {spacing.sm};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {colors.surface};
        border-radius: {radius.md};
        padding: {spacing.sm} {spacing.lg};
        transition: all {transitions.base} {transitions.ease};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {colors.surface_variant};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {colors.primary} !important;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background-color: {colors.primary};
    }}
    
    /* Tooltips */
    .tooltip {{
        position: relative;
        display: inline-block;
    }}
    
    .tooltip .tooltiptext {{
        visibility: hidden;
        background-color: {colors.surface};
        color: {colors.text_primary};
        text-align: center;
        border-radius: {radius.md};
        padding: {spacing.sm};
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity {transitions.base};
        border: 1px solid {colors.border};
    }}
    
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    
    /* ==================== RESPONSIVIDAD ==================== */
    
    /* Tablets y pantallas pequeñas (< 1024px) */
    @media (max-width: 1024px) {{
        .main-header {{
            padding: {spacing.md};
            font-size: {typo.size_lg};
        }}
        
        .metric-card, .card {{
            padding: {spacing.md};
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: {typo.size_xl};
        }}
        
        /* Ajustar sidebar en tablets */
        section[data-testid="stSidebar"] {{
            width: 250px !important;
        }}
    }}
    
    /* Móviles (< 768px) */
    @media (max-width: 768px) {{
        .main-header {{
            padding: {spacing.sm};
            font-size: {typo.size_base};
        }}
        
        .metric-card, .card {{
            padding: {spacing.sm};
            margin: {spacing.sm} 0;
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: {typo.size_lg};
        }}
        
        .stButton > button {{
            width: 100%;
            padding: {spacing.sm};
        }}
        
        /* Forzar columnas a stack en móvil */
        [data-testid="column"] {{
            width: 100% !important;
            flex: 0 0 100% !important;
        }}
        
        /* Hacer sidebar colapsable por defecto */
        section[data-testid="stSidebar"] {{
            width: 0 !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="true"] {{
            width: 80% !important;
        }}
        
        /* Tabs responsivos */
        .stTabs [data-baseweb="tab"] {{
            padding: {spacing.xs} {spacing.sm};
            font-size: {typo.size_sm};
        }}
    }}
    
    /* Pantallas muy pequeñas (< 480px) */
    @media (max-width: 480px) {{
        .main-header {{
            font-size: {typo.size_sm};
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: {typo.size_base};
        }}
        
        /* Reducir padding en elementos */
        .metric-card, .card {{
            padding: {spacing.xs};
        }}
        
        /* Hacer inputs más grandes para móvil */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            font-size: 16px !important; /* Evita zoom en iOS */
        }}
    }}
    
    /* Pantallas grandes (> 1920px) */
    @media (min-width: 1920px) {{
        .main-header {{
            padding: {spacing.xl};
            font-size: {typo.size_3xl};
        }}
        
        .metric-card, .card {{
            padding: {spacing.xl};
        }}
    }}
    
    /* Mejoras para impresión */
    @media print {{
        section[data-testid="stSidebar"] {{
            display: none !important;
        }}
        
        .stButton {{
            display: none !important;
        }}
        
        .main-header {{
            background: white;
            color: black;
        }}
    }}
</style>
    """


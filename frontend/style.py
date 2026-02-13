"""
Configuración de estilos y tema de la aplicación.
CSS profesional con botones semánticos, glassmorphism y diseño atractivo.
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
    css = generate_custom_css()
    st.markdown(css, unsafe_allow_html=True)


def generate_custom_css() -> str:
    """Generar CSS personalizado usando el sistema de tema."""
    colors = theme.colors
    typo = theme.typography
    spacing = theme.spacing
    radius = theme.radius
    transitions = theme.transitions

    return f"""
<style>
    /* ═══════════════════════ VARIABLES CSS ═══════════════════════ */
    {theme.generate_css()}

    /* ═══════════════════════ GOOGLE FONTS ═══════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ═══════════════════════ ESTILOS GLOBALES ═══════════════════════ */
    html, body, [data-testid="stAppViewContainer"] {{
        color: {colors.text_primary};
        font-family: {typo.font_family};
        background-color: {colors.background};
    }}

    /* Fondo con patrón sutil */
    [data-testid="stAppViewContainer"] > .main {{
        background:
            {colors.gradient_glow},
            {colors.background};
    }}

    /* ═══════════════════════ HEADERS ═══════════════════════ */
    .main-header {{
        font-family: {typo.font_family};
        background: {colors.gradient_primary};
        padding: {spacing.lg} {spacing.xl};
        border-radius: {radius.xl};
        color: white;
        text-align: center;
        margin-bottom: {spacing.xl};
        box-shadow: {theme.shadows.lg}, {theme.shadows.glow};
        position: relative;
        overflow: hidden;
    }}

    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
        pointer-events: none;
    }}

    /* ═══════════════════════ CARDS GLASSMORPHISM ═══════════════════════ */
    .metric-card {{
        background: {colors.gradient_card};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: {spacing.lg};
        border-radius: {radius.xl};
        box-shadow: {theme.shadows.md};
        margin: {spacing.md} 0;
        transition: all {transitions.base} {transitions.ease};
        border: 1px solid {colors.border};
        position: relative;
        overflow: hidden;
    }}

    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: {colors.gradient_primary};
        opacity: 0;
        transition: opacity {transitions.base} {transitions.ease};
    }}

    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: {theme.shadows.lg}, {theme.shadows.glow};
        border-color: {colors.border_active};
    }}

    .metric-card:hover::before {{
        opacity: 1;
    }}

    .card {{
        background: {colors.gradient_card};
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: {spacing.lg};
        border-radius: {radius.xl};
        box-shadow: {theme.shadows.sm};
        margin-bottom: {spacing.lg};
        border: 1px solid {colors.border};
    }}

    /* ═══════════════════════ BOTONES BASE ═══════════════════════ */
    .stButton > button {{
        background: {colors.gradient_card} !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_primary} !important;
        padding: {spacing.sm} {spacing.lg} !important;
        border-radius: {radius.md} !important;
        box-shadow: {theme.shadows.sm} !important;
        transition: all {transitions.base} {transitions.ease} !important;
        font-weight: {typo.weight_medium} !important;
        font-family: {typo.font_family} !important;
        backdrop-filter: blur(8px) !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .stButton > button:hover {{
        background: {colors.gradient_accent} !important;
        border-color: {colors.primary} !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: {theme.shadows.md}, {theme.shadows.glow} !important;
    }}

    .stButton > button:active {{
        transform: translateY(0) !important;
        box-shadow: {theme.shadows.sm} !important;
    }}

    .stButton > button:focus {{
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
        outline: none !important;
    }}

    /* ── Botón Primary (Streamlit type="primary") ── */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {{
        background: {colors.gradient_primary} !important;
        border: 1px solid {colors.primary} !important;
        color: #FFFFFF !important;
        font-weight: {typo.weight_semibold} !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {{
        background: linear-gradient(135deg, #1CA8D4 0%, #1383A7 100%) !important;
        border-color: {colors.primary_light} !important;
        color: #FFFFFF !important;
        box-shadow: {theme.shadows.lg}, 0 0 25px rgba(19,131,167,0.3) !important;
    }}

    /* ── Botón Secondary ── */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {{
        background: transparent !important;
        border: 1px solid {colors.border} !important;
        color: {colors.primary_light} !important;
    }}

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: rgba(19, 131, 167, 0.1) !important;
        border-color: {colors.primary} !important;
        color: #FFFFFF !important;
    }}

    /* ═══════════════ BOTONES SEMÁNTICOS (por contenido) ═══════════════ */

    /* Botones INICIAR / ACEPTAR / CONFIRMAR → Verde */
    .stButton > button:has(> div:where(:is([data-testid])):empty) {{
        /* fallback */
    }}

    /* Download buttons */
    .stDownloadButton > button {{
        background: {colors.gradient_primary} !important;
        border: 1px solid {colors.primary} !important;
        color: #FFFFFF !important;
        border-radius: {radius.md} !important;
        font-weight: {typo.weight_medium} !important;
        transition: all {transitions.base} {transitions.ease} !important;
    }}

    .stDownloadButton > button:hover {{
        background: linear-gradient(135deg, #1CA8D4 0%, #1383A7 100%) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: {theme.shadows.md}, {theme.shadows.glow} !important;
    }}

    /* ═══════════════════════ INPUTS ═══════════════════════ */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        color: {colors.text_primary} !important;
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
        transition: all {transitions.base} {transitions.ease} !important;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
    }}

    /* Select boxes */
    .stSelectbox > div > div {{
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
    }}

    /* ═══════════════════════ SLIDERS (umbrales dev) ═══════════════════════ */
    /* Track del slider */
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, {colors.secondary} 0%, {colors.primary} 100%) !important;
    }}

    /* Slider - parte recorrida (fill) */
    .stSlider [data-baseweb="slider"] [role="slider"] {{
        background-color: {colors.primary_light} !important;
        border-color: {colors.primary_light} !important;
        box-shadow: 0 0 8px {colors.primary_glow} !important;
    }}

    /* Slider track base */
    .stSlider div[data-baseweb="slider"] > div:first-child {{
        background: {colors.surface_elevated} !important;
    }}

    /* Slider track fill (activo/recorrido) */
    .stSlider div[data-baseweb="slider"] > div:first-child > div {{
        background: linear-gradient(90deg, {colors.primary} 0%, {colors.primary_light} 100%) !important;
    }}

    /* Slider thumb */
    .stSlider div[data-baseweb="slider"] div[role="slider"] {{
        background: {colors.primary_light} !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0 0 12px {colors.primary_glow}, {theme.shadows.md} !important;
        width: 20px !important;
        height: 20px !important;
    }}

    .stSlider div[data-baseweb="slider"] div[role="slider"]:hover {{
        background: #FFFFFF !important;
        border-color: {colors.primary_light} !important;
        transform: scale(1.15) !important;
    }}

    /* Slider labels */
    .stSlider label {{
        color: {colors.text_primary} !important;
    }}

    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {{
        color: {colors.text_secondary} !important;
    }}

    /* ═══════════════════════ TOGGLE / SWITCH ═══════════════════════ */
    .stToggle label span[data-baseweb="toggle-track"] {{
        background-color: {colors.surface_elevated} !important;
    }}

    .stToggle label input:checked + span[data-baseweb="toggle-track"] {{
        background-color: {colors.primary} !important;
    }}

    /* ═══════════════════════ POPOVER (dev options) ═══════════════════════ */
    [data-testid="stPopover"] {{
        background: {colors.surface} !important;
        border: 1px solid {colors.border_active} !important;
        border-radius: {radius.xl} !important;
        box-shadow: {theme.shadows.xl} !important;
    }}

    [data-testid="stPopover"] .stSlider label {{
        color: {colors.text_primary} !important;
        font-weight: {typo.weight_medium} !important;
    }}

    [data-testid="stPopoverBody"] {{
        background: {colors.surface} !important;
        padding: {spacing.md} !important;
    }}

    /* ═══════════════════════ ALERTS ═══════════════════════ */
    .stAlert {{
        background-color: {colors.surface_variant} !important;
        color: {colors.text_primary} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
        padding: {spacing.md} !important;
        backdrop-filter: blur(8px) !important;
    }}

    /* ═══════════════════════ DATAFRAMES ═══════════════════════ */
    .stDataFrame {{
        color: {colors.text_primary};
        border-radius: {radius.md};
        overflow: hidden;
    }}

    /* ═══════════════════════ EXPANDERS ═══════════════════════ */
    .streamlit-expanderHeader {{
        background-color: {colors.surface_variant} !important;
        color: {colors.text_primary} !important;
        border-radius: {radius.md} !important;
        padding: {spacing.md} !important;
        border: 1px solid {colors.border_subtle} !important;
        transition: all {transitions.base} {transitions.ease} !important;
    }}

    .streamlit-expanderHeader:hover {{
        border-color: {colors.border_active} !important;
        background-color: rgba(19, 131, 167, 0.12) !important;
    }}

    /* ═══════════════════════ ANIMACIONES ═══════════════════════ */
    .notification {{
        padding: {spacing.md};
        border-radius: {radius.md};
        margin-bottom: {spacing.md};
        animation: slideIn {transitions.slow} {transitions.ease};
    }}

    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}

    .success-animation {{
        animation: pulse 1.5s ease-in-out infinite;
    }}

    /* ═══════════════════════ SCROLLBAR ═══════════════════════ */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}

    ::-webkit-scrollbar-track {{
        background: {colors.surface};
        border-radius: {radius.full};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {colors.border_active};
        border-radius: {radius.full};
        transition: background {transitions.base};
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {colors.primary};
    }}

    /* ═══════════════════════ SIDEBAR ═══════════════════════ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {colors.surface} 0%, {colors.background} 100%);
        border-right: 1px solid {colors.border_subtle};
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_primary} !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(19, 131, 167, 0.12) !important;
        border-color: {colors.primary} !important;
        color: #FFFFFF !important;
    }}

    /* option_menu styles */
    section[data-testid="stSidebar"] .nav-link {{
        color: {colors.text_secondary} !important;
        border-radius: {radius.md} !important;
        transition: all {transitions.base} {transitions.ease} !important;
    }}

    section[data-testid="stSidebar"] .nav-link:hover {{
        color: {colors.text_primary} !important;
        background: rgba(19, 131, 167, 0.10) !important;
    }}

    section[data-testid="stSidebar"] .nav-link-selected {{
        background: {colors.gradient_primary} !important;
        color: #FFFFFF !important;
    }}

    /* ═══════════════════════ METRICS ═══════════════════════ */
    [data-testid="stMetricValue"] {{
        font-size: {typo.size_2xl};
        font-weight: {typo.weight_bold};
        color: {colors.primary_light};
    }}

    [data-testid="stMetricLabel"] {{
        color: {colors.text_secondary};
    }}

    /* ═══════════════════════ TABS ═══════════════════════ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {spacing.xs};
        background: {colors.surface};
        padding: 4px;
        border-radius: {radius.lg};
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: {radius.md};
        padding: {spacing.sm} {spacing.lg};
        transition: all {transitions.base} {transitions.ease};
        color: {colors.text_secondary} !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(19, 131, 167, 0.10);
        color: {colors.text_primary} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {colors.gradient_primary} !important;
        color: #FFFFFF !important;
        box-shadow: {theme.shadows.sm};
    }}

    /* Tab highlight bar - remover */
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* ═══════════════════════ PROGRESS BAR ═══════════════════════ */
    @keyframes progressShimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    .stProgress > div > div > div {{
        background: linear-gradient(
            90deg,
            {colors.primary_dark} 0%,
            {colors.primary} 25%,
            rgba(240, 250, 254, 0.85) 50%,
            {colors.primary} 75%,
            {colors.primary_dark} 100%
        ) !important;
        background-size: 200% 100% !important;
        animation: progressShimmer 2s ease-in-out infinite !important;
        border-radius: {radius.full} !important;
        box-shadow: 0 0 12px rgba(19, 131, 167, 0.4),
                    0 0 4px rgba(240, 250, 254, 0.3) !important;
    }}

    .stProgress > div > div {{
        background: {colors.surface_elevated} !important;
        border-radius: {radius.full} !important;
        border: 1px solid rgba(19, 131, 167, 0.15) !important;
        overflow: hidden !important;
    }}

    /* Texto de la progress bar */
    .stProgress p {{
        color: rgba(240, 250, 254, 0.8) !important;
        font-weight: 500 !important;
    }}

    /* ═══════════════════════ FILE UPLOADER ═══════════════════════ */
    [data-testid="stFileUploader"] {{
        border: 2px dashed {colors.border} !important;
        border-radius: {radius.xl} !important;
        background: {colors.surface_variant} !important;
        transition: all {transitions.base} {transitions.ease} !important;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: {colors.primary} !important;
        background: rgba(19, 131, 167, 0.06) !important;
    }}

    /* ═══════════════════════ FORM ═══════════════════════ */
    [data-testid="stForm"] {{
        background: {colors.surface_variant} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.xl} !important;
        padding: {spacing.lg} !important;
    }}

    /* ═══════════════════════ DIVIDER ═══════════════════════ */
    hr {{
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, {colors.border_active}, transparent) !important;
        margin: {spacing.xl} 0 !important;
    }}

    /* ═══════════════════════ MULTISELECT ═══════════════════════ */
    .stMultiSelect [data-baseweb="tag"] {{
        background: {colors.gradient_primary} !important;
        border: none !important;
        border-radius: {radius.sm} !important;
        color: #FFFFFF !important;
    }}

    /* ═══════════════════════ TOOLTIPS ═══════════════════════ */
    .tooltip .tooltiptext {{
        background-color: {colors.surface_elevated};
        color: {colors.text_primary};
        border-radius: {radius.md};
        padding: {spacing.sm};
        border: 1px solid {colors.border};
    }}

    /* ═══════════════════════ RESPONSIVIDAD ═══════════════════════ */

    @media (max-width: 1024px) {{
        .main-header {{
            padding: {spacing.md};
        }}
        .metric-card, .card {{
            padding: {spacing.md};
        }}
        [data-testid="stMetricValue"] {{
            font-size: {typo.size_xl};
        }}
        section[data-testid="stSidebar"] {{
            width: 250px !important;
        }}
    }}

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
            width: 100% !important;
            padding: {spacing.sm} !important;
        }}
        [data-testid="column"] {{
            width: 100% !important;
            flex: 0 0 100% !important;
        }}
        section[data-testid="stSidebar"] {{
            width: 0 !important;
        }}
        section[data-testid="stSidebar"][aria-expanded="true"] {{
            width: 80% !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding: {spacing.xs} {spacing.sm} !important;
            font-size: {typo.size_sm} !important;
        }}
    }}

    @media (max-width: 480px) {{
        .main-header {{
            font-size: {typo.size_sm};
        }}
        [data-testid="stMetricValue"] {{
            font-size: {typo.size_base};
        }}
        .metric-card, .card {{
            padding: {spacing.xs};
        }}
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            font-size: 16px !important;
        }}
    }}

    @media (min-width: 1920px) {{
        .main-header {{
            padding: {spacing.xl};
            font-size: {typo.size_3xl};
        }}
        .metric-card, .card {{
            padding: {spacing.xl};
        }}
    }}

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

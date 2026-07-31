"""
Configuración de estilos y tema de la aplicación.
CSS profesional con botones semánticos, glassmorphism y diseño atractivo.
Soporta tema oscuro y claro dinámicamente.
"""

import streamlit as st
from config.theme import get_current_theme


def setup_page_and_style():
    """Configurar página y aplicar estilos del tema."""
    st.set_page_config(
        page_title="Sistema IDS IoT - Detección de Intrusiones",
        page_icon="🛡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Inicializar tema si no existe
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    
    t = get_current_theme()
    css = generate_custom_css(t)
    st.markdown(css, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _generate_css_cached(theme_mode: str) -> str:
    """Genera y cachea el CSS por modo de tema (solo se regenera al cambiar tema)."""
    from config.theme import get_theme_by_mode
    theme = get_theme_by_mode(theme_mode)
    return _build_css(theme)


def generate_custom_css(theme=None) -> str:
    """Generar CSS personalizado usando el sistema de tema (cacheado)."""
    theme_mode = st.session_state.get("theme_mode", "dark")
    return _generate_css_cached(theme_mode)


def _build_css(theme) -> str:
    """Construye el CSS completo a partir del tema."""
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
        overflow-x: hidden !important;
    }}

    /* Fondo con patrón sutil */
    [data-testid="stAppViewContainer"] > .main {{
        background:
            {colors.gradient_glow},
            {colors.background};
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    /* Evitar desborde horizontal en bloques de contenido */
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    .stMarkdown,
    [data-testid="column"] {{
        overflow-x: hidden !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}

    /* ═══ Fix: Plotly resize loop dentro de st.columns ═══ */
    [data-testid="stPlotlyChart"],
    .stPlotlyChart {{
        max-width: 100% !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}
    [data-testid="stPlotlyChart"] > div {{
        max-width: 100% !important;
        width: 100% !important;
    }}
    [data-testid="stPlotlyChart"] iframe {{
        max-width: 100% !important;
        width: 100% !important;
    }}
    .js-plotly-plot, .plot-container, .plotly {{
        max-width: 100% !important;
        width: 100% !important;
    }}

    /* ═══ Fix: st.dataframe dentro de columnas ═══ */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] > div {{
        max-width: 100% !important;
        overflow-x: auto !important;
    }}

    /* ═══ Fix: HTML embebido (st.markdown) ═══ */
    [data-testid="stMarkdownContainer"] {{
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
    }}
    [data-testid="stMarkdownContainer"] table {{
        max-width: 100% !important;
        table-layout: fixed !important;
    }}
    [data-testid="stMarkdownContainer"] div {{
        max-width: 100% !important;
        box-sizing: border-box !important;
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
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
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
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
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
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;        font-weight: {typo.weight_medium} !important;
        font-family: {typo.font_family} !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .stButton > button:hover {{
        background: {colors.gradient_accent} !important;
        border-color: {colors.primary} !important;
        color: {colors.text_on_primary} !important;
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
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        font-weight: {typo.weight_semibold} !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {{
        background: {colors.gradient_primary} !important;
        border-color: {colors.primary_light} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        box-shadow: {theme.shadows.lg}, 0 0 25px {colors.primary_glow} !important;
    }}

    /* Primary button disabled */
    .stButton > button[kind="primary"]:disabled,
    .stButton > button[data-testid="baseButton-primary"]:disabled {{
        background: {colors.gradient_primary} !important;
        border: 1px solid {colors.primary} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        opacity: 0.5 !important;
    }}

    /* ── Botón Secondary (blanco/superficie, NO azul) ── */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"],
    .stMainBlockContainer .stButton > button[kind="secondary"],
    .stMainBlockContainer .stButton > button[data-testid="baseButton-secondary"],
    section[data-testid="stMain"] .stButton > button[kind="secondary"],
    section[data-testid="stMain"] .stButton > button[data-testid="baseButton-secondary"] {{
        background: {colors.surface} !important;
        background-image: none !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
        box-shadow: none !important;
    }}

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: {colors.surface_elevated} !important;
        background-image: none !important;
        border-color: {colors.primary} !important;
        color: {colors.primary} !important;
        -webkit-text-fill-color: {colors.primary} !important;
    }}

    .stButton > button[kind="secondary"]:disabled,
    .stButton > button[data-testid="baseButton-secondary"]:disabled {{
        background: {colors.surface} !important;
        background-image: none !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_disabled} !important;
        -webkit-text-fill-color: {colors.text_disabled} !important;
        opacity: 0.6 !important;
    }}

    /* ── Botón disabled genérico: texto blanco (excepto secondary) ── */
    .stButton > button:disabled:not([kind="secondary"]):not([data-testid="baseButton-secondary"]) {{
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
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
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        border-radius: {radius.md} !important;
        font-weight: {typo.weight_medium} !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;
    }}

    .stDownloadButton > button:hover {{
        background: {colors.gradient_primary} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        transform: translateY(-2px) !important;
        box-shadow: {theme.shadows.md}, {theme.shadows.glow} !important;
    }}

    .stDownloadButton > button:disabled {{
        background: {colors.gradient_primary} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
        opacity: 0.5 !important;
    }}

    /* ═══════════════════════ INPUTS ═══════════════════════ */
    .stTextInput > div > div > input {{
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
    }}

    /* ── Number Input: COMPLETO ── */
    /* Contenedor exterior */
    .stNumberInput {{
        color: {colors.text_primary} !important;
    }}
    /* Label */
    .stNumberInput label,
    .stNumberInput label p,
    .stNumberInput label span {{
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
    }}
    /* Wrapper baseweb */
    .stNumberInput [data-baseweb="input"],
    .stNumberInput > div,
    .stNumberInput > div > div,
    .stNumberInput > div > div > div {{
        background-color: {colors.surface_elevated} !important;
        background: {colors.surface_elevated} !important;
        border-color: {colors.border} !important;
        border-radius: {radius.md} !important;
    }}
    .stNumberInput [data-baseweb="input"]:focus-within {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
    }}
    /* El input real donde se escribe */
    .stNumberInput [data-baseweb="input"] input,
    .stNumberInput > div > div > input,
    .stNumberInput input[type="number"],
    .stNumberInput input {{
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
        background-color: transparent !important;
        border: none !important;
        caret-color: {colors.primary} !important;
    }}
    /* Botones +/- del number input */
    .stNumberInput [data-baseweb="input"] button,
    .stNumberInput button {{
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
        border-radius: {radius.sm} !important;
    }}
    .stNumberInput [data-baseweb="input"] button:hover,
    .stNumberInput button:hover {{
        background-color: {colors.primary} !important;
        border-color: {colors.primary} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
    }}
    /* Botones +/- SVG icons */
    .stNumberInput [data-baseweb="input"] button svg,
    .stNumberInput button svg {{
        fill: {colors.text_primary} !important;
        color: {colors.text_primary} !important;
    }}
    .stNumberInput [data-baseweb="input"] button:hover svg,
    .stNumberInput button:hover svg {{
        fill: {colors.text_on_primary} !important;
        color: {colors.text_on_primary} !important;
    }}
    /* Help text */
    .stNumberInput [data-testid="stTooltipIcon"] svg {{
        color: {colors.text_secondary} !important;
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
        border: 3px solid {colors.text_on_primary} !important;
        box-shadow: 0 0 12px {colors.primary_glow}, {theme.shadows.md} !important;
        width: 20px !important;
        height: 20px !important;
    }}

    .stSlider div[data-baseweb="slider"] div[role="slider"]:hover {{
        background: {colors.text_on_primary} !important;
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

    /* Slider thumb value tooltip (cuadro azul con número) */
    .stSlider [data-baseweb="slider"] [data-baseweb="tooltip"],
    .stSlider [data-baseweb="slider"] [role="tooltip"] {{
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }}
    .stSlider [data-baseweb="slider"] [data-baseweb="tooltip"] div,
    .stSlider [data-baseweb="slider"] [role="tooltip"] div {{
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }}
    /* Slider current value display */
    .stSlider div[data-baseweb="slider"] div[role="slider"] div {{
        color: #FFFFFF !important;
        border-radius: 8px !important;
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
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* Popover trigger buttons (the ⚙️ / 👤 buttons in sidebar) */
    section[data-testid="stSidebar"] [data-testid="stPopover"] > div:first-child > button,
    section[data-testid="stSidebar"] [data-testid="stPopover"] button {{
        background: {colors.popover_btn_bg} !important;
        border: 1px solid {colors.popover_btn_border} !important;
        color: {colors.popover_btn_text} !important;
        font-weight: 500 !important;
        border-radius: 22px !important;
        padding: 0.55rem 1.1rem !important;
        width: 100% !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;    }}

    section[data-testid="stSidebar"] [data-testid="stPopover"] > div:first-child > button:hover,
    section[data-testid="stSidebar"] [data-testid="stPopover"] button:hover {{
        background: {colors.popover_btn_hover_bg} !important;
        border-color: {colors.popover_btn_hover_border} !important;
        color: {colors.primary} !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px {colors.primary_glow} !important;
    }}

    [data-testid="stPopover"] .stSlider label {{
        color: {colors.text_primary} !important;
        font-weight: {typo.weight_medium} !important;
    }}

    [data-testid="stPopoverBody"] {{
        background: {colors.popover_body_bg} !important;
        border-radius: 22px !important;
        padding: {spacing.lg} !important;
        border: 1px solid {colors.popover_body_border} !important;
        box-shadow: {colors.popover_body_shadow} !important;
    }}

    /* ═══════════════════════ ALERTS ═══════════════════════ */
    .stAlert {{
        background-color: {colors.surface_variant} !important;
        color: {colors.text_primary} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
        padding: {spacing.md} !important;
        backdrop-filter: blur(4px) !important;
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
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;    }}

    .streamlit-expanderHeader:hover {{
        border-color: {colors.border_active} !important;
        background-color: {colors.surface_variant} !important;
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
        background: linear-gradient(180deg, {colors.surface} 0%, {colors.background} 100%) !important;
        border-right: 1px solid {colors.border_subtle} !important;
    }}

    /* Sidebar inner container background */
    section[data-testid="stSidebar"] > div {{
        background-color: transparent !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        background-color: transparent !important;
    }}

    /* Sidebar text elements */
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label {{
        color: {colors.text_primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: {colors.text_secondary} !important;
    }}

    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {{
        background: linear-gradient(90deg, transparent, {colors.border_active}, transparent) !important;
    }}

    /* ── Sidebar buttons (popover triggers: Configuración avanzada, etc.) ── */
    section[data-testid="stSidebar"] .stButton > button {{
        background: {colors.popover_btn_bg} !important;
        border: 1px solid {colors.popover_btn_border} !important;
        color: {colors.popover_btn_text} !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: {colors.popover_btn_hover_bg} !important;
        border-color: {colors.popover_btn_hover_border} !important;
        color: {colors.primary} !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px {colors.primary_glow} !important;
    }}

    /* Sidebar selectbox */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: {colors.surface} !important;
        border-color: {colors.border} !important;
        color: {colors.text_primary} !important;
    }}

    /* Sidebar toggles/sliders labels */
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
        color: {colors.text_primary} !important;
    }}

    /* ── Sidebar navigation buttons (custom nav) ── */
    section[data-testid="stSidebar"] .stButton > button {{
        border-radius: 14px !important;
        font-size: 0.97rem !important;
        text-align: left !important;
        padding: 0.55rem 1rem !important;
        margin: 2px 0 !important;
        border: none !important;
        background: transparent !important;
        color: {colors.nav_text} !important;
        font-weight: 400 !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;        justify-content: flex-start !important;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: {colors.nav_hover} !important;
        color: {colors.primary} !important;
    }}
    /* Active nav button (disabled state used for active indicator) */
    section[data-testid="stSidebar"] .stButton > button:disabled,
    section[data-testid="stSidebar"] .stButton > button:disabled p,
    section[data-testid="stSidebar"] .stButton > button:disabled span,
    section[data-testid="stSidebar"] .stButton > button:disabled div,
    section[data-testid="stSidebar"] .stButton > button[disabled] {{
        background: {colors.nav_selected_bg} !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px {colors.primary_glow} !important;
        border: none !important;
        opacity: 1 !important;
        cursor: default !important;
    }}

    /* ── Theme toggle button special style ── */
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {{
        background: {colors.surface_variant} !important;
        border: 1px solid {colors.border} !important;
        color: {colors.text_primary} !important;
    }}

    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: {colors.surface_overlay} !important;
        border-color: {colors.primary} !important;
        color: {colors.primary} !important;
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
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease};
        color: {colors.text_secondary} !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {colors.surface_overlay};
        color: {colors.text_primary} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {colors.gradient_primary} !important;
        color: {colors.text_on_primary} !important;
        -webkit-text-fill-color: {colors.text_on_primary} !important;
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
            {colors.text_primary} 50%,
            {colors.primary} 75%,
            {colors.primary_dark} 100%
        ) !important;
        background-size: 200% 100% !important;
        animation: progressShimmer 2s ease-in-out infinite !important;
        border-radius: {radius.full} !important;
        box-shadow: 0 0 12px {colors.primary_glow},
                    0 0 4px {colors.primary_glow} !important;
    }}

    .stProgress > div > div {{
        background: {colors.surface_elevated} !important;
        border-radius: {radius.full} !important;
        border: 1px solid {colors.border_subtle} !important;
        overflow: hidden !important;
    }}

    /* Texto de la progress bar */
    .stProgress p {{
        color: {colors.text_secondary} !important;
        font-weight: 500 !important;
    }}

    /* ═══════════════════════ FILE UPLOADER ═══════════════════════ */
    [data-testid="stFileUploader"] {{
        border: 2px dashed {colors.border} !important;
        border-radius: {radius.xl} !important;
        background: {colors.surface_variant} !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: {colors.primary} !important;
        background: {colors.surface_overlay} !important;
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
        color: {colors.text_on_primary} !important;
    }}

    /* ═══════════════════════ TOOLTIPS ═══════════════════════ */
    .tooltip .tooltiptext {{
        background-color: {colors.surface_elevated};
        color: {colors.text_primary};
        border-radius: {radius.md};
        padding: {spacing.sm};
        border: 1px solid {colors.border};
    }}

    /* Tooltips globales (help="..." de botones, inputs, etc.) */
    [data-baseweb="tooltip"],
    [data-baseweb="tooltip"] [role="tooltip"],
    [role="tooltip"],
    [data-testid="stTooltipContent"],
    div[data-baseweb="popover"] > div {{
        background-color: {colors.surface_elevated} !important;
        color: {colors.text_primary} !important;
        border: 1px solid {colors.border} !important;
        border-radius: {radius.md} !important;
    }}
    [data-baseweb="tooltip"] p,
    [data-baseweb="tooltip"] span,
    [data-baseweb="tooltip"] div,
    [role="tooltip"] p,
    [role="tooltip"] span,
    [role="tooltip"] div,
    [data-testid="stTooltipContent"] p,
    [data-testid="stTooltipContent"] span,
    div[data-baseweb="popover"] > div p,
    div[data-baseweb="popover"] > div span {{
        color: {colors.text_primary} !important;
        -webkit-text-fill-color: {colors.text_primary} !important;
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

    /* ═══════════════════════ WIDGET OVERRIDES (config.toml) ═══════════════════════ */
    /* Streamlit usa config.toml para colores base de widgets. Los sobreescribimos aquí. */

    /* Selectbox / dropdown container */
    [data-baseweb="select"] > div {{
        background-color: {colors.surface} !important;
        border-color: {colors.border} !important;
    }}
    [data-baseweb="select"] > div > div {{
        color: {colors.text_primary} !important;
    }}
    /* Dropdown menu list */
    /* baseweb popover — selectbox/dropdown only */
    [data-baseweb="popover"] {{
        background-color: {colors.surface} !important;
        border: 1px solid {colors.border} !important;
    }}
    [data-baseweb="popover"] [role="listbox"] {{
        background-color: {colors.surface} !important;
    }}
    [data-baseweb="popover"] [role="option"] {{
        background-color: {colors.surface} !important;
        color: {colors.text_primary} !important;
    }}
    [data-baseweb="popover"] [role="option"]:hover {{
        background-color: {colors.surface_variant} !important;
    }}
    [data-baseweb="popover"] [aria-selected="true"] {{
        background-color: {colors.surface_variant} !important;
    }}

    /* st.popover() body — override baseweb popover when it wraps stPopoverBody */
    [data-baseweb="popover"]:has([data-testid="stPopoverBody"]) {{
        background-color: {colors.popover_body_bg} !important;
        border: 1px solid {colors.popover_body_border} !important;
        border-radius: 22px !important;
        box-shadow: {colors.popover_body_shadow} !important;
    }}

    /* Popover backgrounds (st.popover) */
    [data-testid="stPopover"] > div {{
        background-color: {colors.popover_body_bg} !important;
        border: 1px solid {colors.popover_body_border} !important;
        border-radius: 22px !important;
        box-shadow: {colors.popover_body_shadow} !important;
    }}
    [data-testid="stPopoverBody"] {{
        background-color: {colors.popover_body_bg} !important;
        border-radius: 22px !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] span {{
        color: {colors.text_primary} !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h5 {{
        color: {colors.heading_secondary} !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stWidgetLabel"] label {{
        color: {colors.text_primary} !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] {{
        color: {colors.text_secondary} !important;
    }}

    /* Buttons inside popover body */
    [data-testid="stPopoverBody"] .stButton > button {{
        background: {colors.popover_btn_bg} !important;
        border: 1px solid {colors.popover_btn_border} !important;
        color: {colors.popover_btn_text} !important;
        border-radius: {radius.md} !important;
    }}
    [data-testid="stPopoverBody"] .stButton > button:hover {{
        background: {colors.popover_btn_hover_bg} !important;
        border-color: {colors.popover_btn_hover_border} !important;
        color: {colors.primary} !important;
    }}

    /* Text inputs in popovers */
    [data-testid="stPopoverBody"] .stTextInput > div > div > input {{
        background-color: {colors.surface_elevated} !important;
        color: {colors.text_primary} !important;
        border-color: {colors.border} !important;
        border-radius: {radius.md} !important;
    }}
    [data-testid="stPopoverBody"] .stTextInput > div > div > input:focus {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
    }}

    /* Toggle inside popover */
    [data-testid="stPopoverBody"] .stToggle label span {{  
        color: {colors.text_primary} !important;
    }}

    /* Selectbox inside popover */
    [data-testid="stPopoverBody"] [data-baseweb="select"] > div {{
        background-color: {colors.surface_elevated} !important;
        border-color: {colors.border} !important;
        border-radius: {radius.md} !important;
    }}
    [data-testid="stPopoverBody"] [data-baseweb="select"] > div > div {{
        color: {colors.text_primary} !important;
    }}

    /* Slider track & labels */
    .stSlider [data-baseweb="slider"] div {{
        color: {colors.text_primary} !important;
    }}

    /* Toggle / checkbox */
    .stCheckbox label span {{
        color: {colors.text_primary} !important;
    }}

    /* Number input - see comprehensive section above */

    /* Toast */
    [data-testid="stToast"] {{
        background-color: {colors.surface_elevated} !important;
        color: {colors.text_primary} !important;
        border: 1px solid {colors.border} !important;
    }}

    /* Alert/notification boxes override */
    [data-testid="stAlert"] {{
        color: {colors.text_primary} !important;
    }}

    /* Expander */
    [data-testid="stExpander"] {{
        border-color: {colors.border} !important;
        background-color: {colors.surface_variant} !important;
    }}
    [data-testid="stExpander"] summary {{
        color: {colors.text_primary} !important;
    }}
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {{
        color: {colors.text_primary} !important;
    }}

    /* ── Sidebar expanders (config avanzada / usuario) ── */
    section[data-testid="stSidebar"] [data-testid="stExpander"] {{
        background-color: {colors.popover_body_bg} !important;
        border: 1px solid {colors.popover_btn_border} !important;
        border-radius: 18px !important;
        overflow: hidden;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary {{
        background: {colors.popover_btn_bg} !important;
        color: {colors.popover_btn_text} !important;
        border-radius: 18px !important;
        padding: 0.55rem 1rem !important;
        font-weight: 500 !important;
        transition: background, border-color, box-shadow, color, transform {transitions.base} {transitions.ease} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
        background: {colors.popover_btn_hover_bg} !important;
        color: {colors.primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary svg {{
        fill: {colors.primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        background-color: {colors.popover_body_bg} !important;
        border-top: 1px solid {colors.popover_btn_border} !important;
        padding: 0.8rem !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stMarkdownContainer"] span {{
        color: {colors.text_primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stWidgetLabel"] label {{
        color: {colors.text_primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stCaptionContainer"] {{
        color: {colors.text_secondary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stButton > button {{
        background: {colors.popover_btn_bg} !important;
        border: 1px solid {colors.popover_btn_border} !important;
        color: {colors.popover_btn_text} !important;
        border-radius: 14px !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stButton > button:hover {{
        background: {colors.popover_btn_hover_bg} !important;
        border-color: {colors.popover_btn_hover_border} !important;
        color: {colors.primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stTextInput > div > div > input {{
        background-color: {colors.surface_elevated} !important;
        color: {colors.text_primary} !important;
        border-color: {colors.border} !important;
        border-radius: 10px !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stTextInput > div > div > input:focus {{
        border-color: {colors.primary} !important;
        box-shadow: 0 0 0 3px {colors.primary_glow} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stToggle label span {{
        color: {colors.text_primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-baseweb="select"] > div {{
        background-color: {colors.surface_elevated} !important;
        border-color: {colors.border} !important;
        border-radius: 10px !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] [data-baseweb="select"] > div > div {{
        color: {colors.text_primary} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] hr {{
        border-color: {colors.border} !important;
    }}

    /* DataFrame */
    [data-testid="stDataFrame"] {{
        border: 1px solid {colors.border} !important;
        border-radius: {radius.lg} !important;
    }}

    /* Markdown text */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {{
        color: {colors.text_primary};
    }}
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {{
        color: {colors.heading_primary} !important;
    }}

    /* Hero sections: títulos y subtítulos SIEMPRE blancos */
    .home-hero-content h1, .home-hero-content h2, .home-hero-content h3,
    .home-hero-content p, .home-hero-content strong,
    .home-cta-content h1, .home-cta-content h2, .home-cta-content h3,
    .home-cta-content p, .home-cta-content strong,
    .guia-header-content h1, .guia-header-content h2, .guia-header-content h3,
    .guia-header-content p, .guia-header-content strong,
    .guia-footer-content h1, .guia-footer-content h2, .guia-footer-content h3,
    .guia-footer-content p, .guia-footer-content strong,
    .compare-hero-content h1, .compare-hero-content h2, .compare-hero-content h3,
    .compare-hero-content p, .compare-hero-content strong {{
        color: #FFFFFF !important;
    }}

    /* Caption text */
    [data-testid="stCaptionContainer"] {{
        color: {colors.text_secondary} !important;
    }}

    /* Widget labels (selectbox, slider, etc.) */
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {{
        color: {colors.text_primary} !important;
    }}
</style>
    """

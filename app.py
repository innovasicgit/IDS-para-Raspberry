"""
Aplicación principal - Sistema de Detección de Anomalías IoT.
Punto de entrada y orquestación de la navegación.
"""

import streamlit as st
import sklearn
from streamlit_option_menu import option_menu
from pathlib import Path
from sklearn.metrics import DistanceMetric
import sklearn.metrics._dist_metrics as _dm

# Importar del_columns para que joblib pueda deserializar los modelos
from del_columns import del_columns

# Imports de frontend
from frontend.style import setup_page_and_style
from frontend.auth_ui import ensure_auth
from frontend.pages.dashboard import show_dashboard_page
from frontend.pages.compare import show_compare_page
from frontend.pages.guia import show_guia_page

# Configuración de página y estilos
setup_page_and_style()

# Fix para compatibilidad de modelos pickle
_dm.EuclideanDistance = DistanceMetric.get_metric("euclidean").__class__

# Inicializar estado de sesión
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ==================== AUTENTICACIÓN Y NAVEGACIÓN ====================

# Requerir autenticación para todas las páginas
# ensure_auth()  # DESHABILITADO TEMPORALMENTE

# Simular usuario autenticado para desarrollo
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.username = "admin"

with st.sidebar:
    # Logo
    logo_path = Path(__file__).parent / "img" / "logo.gif"
    st.image(str(logo_path), width=150)
    
    # Info de usuario
    if st.session_state.get("authenticated"):
        st.caption(f"Conectado como: {st.session_state.username}")
        if st.button("Cerrar sesión", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # Menú de navegación
    selected = option_menu(
        "Navegación",
        ["Guía del Sistema", "Panel de Control", "Comparar Modelos"],
        icons=["book", "graph-up", "bar-chart"],
        menu_icon="cast",
        default_index=1
    )

    if selected == "Guía del Sistema":
        st.session_state.page = "guia"
    elif selected == "Panel de Control":
        st.session_state.page = "dashboard"
    else:
        st.session_state.page = "compare"

    # Opciones avanzadas
    st.divider()
    try:
        with st.popover("⚙️ Opciones de desarrollador"):
            st.caption(f"sklearn: {getattr(sklearn, '__version__', 'N/A')}")
            st.session_state.ae_normal_threshold = st.slider(
                "Umbral Normal (Autoencoder)", 
                min_value=0.0, max_value=1.0, value=0.60, step=0.01,
                help="Si la probabilidad de 'Normal' es mayor o igual al umbral, se clasifica como Normal."
            )
            st.session_state.ae_reconstruction_threshold = st.slider(
                "Umbral Reconstrucción (AE)", 
                min_value=0.0, max_value=1.0, value=0.02, step=0.001,
                help="Si el error de reconstrucción es menor o igual al umbral, se considera normal."
            )
            st.session_state.ocsvm_use_sign = st.toggle(
                "OCSVM: usar predicción por signo",
                value=True,
                help="Usa labels del OCSVM (1=inlier, -1=outlier)."
            )
            st.session_state.ocsvm_percentile = st.slider(
                "OCSVM percentil umbral", 
                min_value=0.0, max_value=1.0, value=0.45, step=0.01,
                help="Clasifica como normal si el score ≥ percentil seleccionado."
            )
    except Exception:
        with st.expander("⚙️ Opciones de desarrollador", expanded=False):
            st.caption(f"sklearn: {getattr(sklearn, '__version__', 'N/A')}")
            # ... mismo contenido que arriba ...

# ==================== RENDERIZADO DE PÁGINAS ====================

if st.session_state.page == "guia":
    show_guia_page()
elif st.session_state.page == "dashboard":
    show_dashboard_page()
elif st.session_state.page == "compare":
    show_compare_page()
else:
    # Página por defecto
    show_dashboard_page()

# ==================== FOOTER ====================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🛡 Sistema de Detección de Anomalías IoT</p>
            <p>© 2026 Innovasic | UCC</p>
        </div>
        """,
        unsafe_allow_html=True
    )

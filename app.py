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

# Imports de backend
from backend.notifications_db import NotificationsDB
from config.theme import get_current_theme

# Imports de frontend
from frontend.style import setup_page_and_style
from frontend.auth_ui import ensure_auth
from frontend.home_page import show_home_page
from frontend.pages.dashboard import show_dashboard_page
from frontend.pages.compare import show_compare_page
from frontend.pages.guia import show_guia_page

# Configuración de página y estilos
setup_page_and_style()

# Fix para compatibilidad de modelos pickle
_dm.EuclideanDistance = DistanceMetric.get_metric("euclidean").__class__

# Inicializar estado de sesión
if "page" not in st.session_state:
    st.session_state.page = "home"  # Página de inicio por defecto
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "notifications_db" not in st.session_state:
    st.session_state.notifications_db = NotificationsDB()
    # Cargar configuración guardada
    db = st.session_state.notifications_db
    email_config = db.load_email_config()
    st.session_state.setdefault("user_email", email_config.get("recipient_email", ""))
    st.session_state.setdefault("gmail_user", email_config.get("gmail_user", ""))
    st.session_state.setdefault("gmail_app_password", email_config.get("gmail_app_password", ""))
    st.session_state.setdefault("enable_email_notifications", db.load_preferences())
if "arp_limit_mode" not in st.session_state:
    st.session_state.arp_limit_mode = "medium"

# ==================== AUTENTICACIÓN Y NAVEGACIÓN ====================

# Requerir autenticación para todas las páginas
# ensure_auth()  # DESHABILITADO TEMPORALMENTE

# Simular usuario autenticado para desarrollo
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.username = "admin"

# Obtener tema actual
t = get_current_theme()
c = t.colors

with st.sidebar:
    # Logo
    logo_path = Path(__file__).parent / "img" / "logo.png"
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
        ["Inicio", "Guía del Sistema", "Panel de Control", "Comparar Modelos"],
        icons=["house-fill", "book-half", "shield-shaded", "bar-chart-line-fill"],
        menu_icon="menu-button-wide-fill",
        default_index=0,
        styles={
            "container": {
                "padding": "0.6rem 0.5rem",
                "background-color": c.nav_bg,
                "border-radius": "14px",
                "border": f"1px solid {c.nav_border}",
            },
            "icon": {
                "color": c.primary,
                "font-size": "1.1rem",
            },
            "nav-link": {
                "font-size": "0.95rem",
                "text-align": "left",
                "margin": "3px 0",
                "padding": "0.6rem 1rem",
                "border-radius": "10px",
                "color": c.nav_text,
                "background-color": "transparent",
                "--hover-color": c.nav_hover,
            },
            "nav-link-selected": {
                "background": c.nav_selected_bg,
                "color": c.nav_selected_text,
                "font-weight": "600",
                "box-shadow": f"0 4px 15px {c.primary_glow}",
            },
            "menu-title": {
                "color": c.text_primary,
                "font-size": "0.85rem",
                "font-weight": "600",
                "text-transform": "uppercase",
                "letter-spacing": "0.05em",
                "padding": "0.5rem 1rem",
            },
            "menu-icon": {
                "color": c.primary,
            },
        }
    )

    if selected == "Inicio":
        st.session_state.page = "home"
    elif selected == "Guía del Sistema":
        st.session_state.page = "guia"
    elif selected == "Panel de Control":
        st.session_state.page = "dashboard"
    else:
        st.session_state.page = "compare"

    # Opciones avanzadas
    st.divider()
    try:
        with st.popover("⚙️ Configuración avanzada"):
            st.markdown(f"""
            <div style="margin-bottom: 12px; padding: 8px 12px; 
                        background: {c.gradient_surface}; 
                        border-radius: 8px; border-left: 3px solid {c.primary};">
                <span style="font-size: 0.8rem; color: {c.heading_primary};">🔧 Configuración Avanzada</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"📦 sklearn: `{getattr(sklearn, '__version__', 'N/A')}`")
            
            st.markdown("##### 🤖 Autoencoder")
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
            
            st.markdown("##### 🔵 OCSVM")
            st.session_state.ocsvm_use_sign = st.toggle(
                "Predicción por signo",
                value=True,
                help="Usa labels del OCSVM (1=inlier, -1=outlier)."
            )
            st.session_state.ocsvm_percentile = st.slider(
                "Percentil umbral", 
                min_value=0.0, max_value=1.0, value=0.45, step=0.01,
                help="Clasifica como normal si el score ≥ percentil seleccionado."
            )

        with st.popover("👤 Configuración de usuario"):
            st.markdown(f"""
            <div style="margin-bottom: 12px; padding: 8px 12px; 
                        background: {c.gradient_surface}; 
                        border-radius: 8px; border-left: 3px solid {c.primary};">
                <span style="font-size: 0.8rem; color: {c.heading_primary};">👤 Configuración de Usuario</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 📧 Notificaciones por Email")
            
            db = st.session_state.notifications_db
            
            st.session_state.enable_email_notifications = st.toggle(
                "Activar notificaciones por email",
                value=st.session_state.get("enable_email_notifications", False),
                help="Envía alertas por correo cuando se detectan anomalías en capturas automáticas."
            )
            
            if st.session_state.enable_email_notifications:
                st.session_state.user_email = st.text_input(
                    "📬 Email de destino",
                    value=st.session_state.get("user_email", ""),
                    help="Correo donde recibirás las alertas."
                )
                st.session_state.gmail_user = st.text_input(
                    "👤 Usuario Gmail (remitente)",
                    value=st.session_state.get("gmail_user", ""),
                    help="Cuenta Gmail que enviará los correos."
                )
                
                col_save, col_clear = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar", key="save_email_cfg", use_container_width=True):
                        if st.session_state.user_email and st.session_state.gmail_user:
                            success, msg = db.save_email_config(
                                st.session_state.user_email,
                                st.session_state.gmail_user,
                                st.session_state.get("gmail_app_password", "")
                            )
                            db.save_preferences(True)
                            st.toast(msg)
                        else:
                            st.toast("⚠️ Completa todos los campos")
                with col_clear:
                    if st.button("🗑️ Limpiar", key="clear_email_cfg", use_container_width=True):
                        db.delete_email_config()
                        st.session_state.user_email = ""
                        st.session_state.gmail_user = ""
                        st.session_state.gmail_app_password = ""
                        st.session_state.enable_email_notifications = False
                        db.save_preferences(False)
                        st.toast("✅ Configuración eliminada")
                        st.rerun()
            else:
                db.save_preferences(False)

            st.markdown("---")
            st.markdown("##### 🛡️ Filtro ARP")
            st.session_state.arp_limit_mode = st.selectbox(
                "Modo de límite ARP",
                options=["low", "medium", "high", "none"],
                index=["low", "medium", "high", "none"].index(
                    st.session_state.get("arp_limit_mode", "medium")
                ),
                help="Controla cuántos paquetes ARP se permiten antes de alertar."
            )
    except Exception:
        with st.expander("⚙️ Configuración avanzada", expanded=False):
            st.caption(f"sklearn: {getattr(sklearn, '__version__', 'N/A')}")

    # Toggle de tema claro/oscuro
    st.divider()
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    theme_label = "🌙 Modo Oscuro" if is_dark else "☀️ Modo Claro"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "light" if is_dark else "dark"
        st.rerun()

# ==================== RENDERIZADO DE PÁGINAS ====================

if st.session_state.page == "home":
    show_home_page()
elif st.session_state.page == "guia":
    show_guia_page()
elif st.session_state.page == "dashboard":
    show_dashboard_page()
elif st.session_state.page == "compare":
    show_compare_page()
else:
    # Página por defecto
    show_home_page()

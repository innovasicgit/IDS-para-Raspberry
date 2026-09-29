import streamlit as st
import sklearn
from pathlib import Path
from sklearn.metrics import DistanceMetric
import sklearn.metrics._dist_metrics as _dm

# Importar del_columns para que joblib pueda deserializar los modelos
from del_columns import del_columns

# Importar AutoencoderClassifier para que joblib pueda deserializar autoencoder.pkl
# El archivo "autoencoder_classifier.py" en la raíz actúa como módulo puente;
# internamente reexporta la clase desde `backend.autoencoderclassifier`. De esta
# forma los modelos serializados con ese nombre siguen cargando correctamente.
from autoencoder_classifier import AutoencoderClassifier

# Imports de backend
from backend.notifications_db import NotificationsDB
from backend.notifications import NotificationManager
from config.theme import get_current_theme
from config.i18n import SUPPORTED_LANGUAGES, get_language, t

# Imports de frontend
from frontend.style import setup_page_and_style
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
if 'notification_manager' not in st.session_state:
    st.session_state.notification_manager = NotificationManager()
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
theme = get_current_theme()
c = theme.colors

with st.sidebar:
    selected_language = st.selectbox(
        t("language"),
        options=list(SUPPORTED_LANGUAGES),
        format_func=SUPPORTED_LANGUAGES.get,
        index=list(SUPPORTED_LANGUAGES).index(get_language()),
        key="language_selector",
    )
    if selected_language != get_language():
        st.session_state.language = selected_language
        st.rerun()

    # Logo centrado (cacheado en session_state para no re-leer del disco)
    if "_logo_b64" not in st.session_state:
        import base64
        _logo_path = Path(__file__).parent / "img" / "logo.png"
        if _logo_path.exists():
            with open(_logo_path, "rb") as _f:
                st.session_state._logo_b64 = base64.b64encode(_f.read()).decode()
        else:
            st.session_state._logo_b64 = None
    
    if st.session_state._logo_b64:
        st.markdown(f"""
        <div style='display:flex;justify-content:center;align-items:center;width:100%;margin-bottom:0.5rem;'>
            <img src='data:image/png;base64,{st.session_state._logo_b64}' width='150' style='display:block;margin:0 auto;border-radius:22px;'/>
        </div>
        """, unsafe_allow_html=True)
    
    # Info de usuario
    if st.session_state.get("authenticated"):
        st.caption(t("connected_as", username=st.session_state.username))
        if st.button(t("logout"), key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # ── Menú de navegación nativo (sin iframe, respeta el tema) ──
    _nav_items = [
        (t("home"), "home"),
        (t("guide"), "guia"),
        (t("dashboard"), "dashboard"),
        (t("compare"), "compare"),
    ]
    
    # Título de sección
    st.markdown(f"""
    <p style="
        font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.05em; color: {c.text_secondary};
        padding: 0.3rem 0.2rem; margin: 0 0 0.3rem 0;
    ">{t("navigation")}</p>
    """, unsafe_allow_html=True)
    
    # Contenedor visual con borde redondeado
    nav_container = st.container()
    with nav_container:
        for label, page_key in _nav_items:
            is_active = st.session_state.page == page_key
            # Inyectar estilo activo justo antes del botón
            if is_active:
                st.markdown(f"""
                <style>
                    /* Estilo para el botón de navegación activo: {page_key} */
                    div[data-testid="stVerticalBlockBorderWrapper"]:has(button[kind="secondary"]) 
                    button[kind="secondary"]:disabled {{
                        background: {c.nav_selected_bg} !important;
                        color: {c.nav_selected_text} !important;
                        font-weight: 600 !important;
                        box-shadow: 0 4px 15px {c.primary_glow} !important;
                        border: none !important;
                        opacity: 1 !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
                st.button(label, key=f"nav_{page_key}", use_container_width=True, disabled=True)
            else:
                if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()

    # Opciones avanzadas
    st.divider()

    with st.expander(t("advanced_settings"), expanded=False):
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>{t('autoencoder')}</p>", unsafe_allow_html=True)
        st.session_state.ae_normal_threshold = st.slider(
            t("normal_threshold"),
            min_value=0.0, max_value=1.0, value=0.60, step=0.01,
            help=t("normal_threshold_help")
        )
        st.session_state.ae_reconstruction_threshold = st.slider(
            t("reconstruction_threshold"),
            min_value=0.0, max_value=1.0, value=0.02, step=0.001,
            help=t("reconstruction_threshold_help")
        )
        
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>{t('ocsvm')}</p>", unsafe_allow_html=True)
        st.session_state.ocsvm_use_sign = st.toggle(
            t("sign_prediction"),
            value=True,
            help=t("sign_prediction_help")
        )
        st.session_state.ocsvm_percentile = st.slider(
            t("percentile_threshold"),
            min_value=0.0, max_value=1.0, value=0.45, step=0.01,
            help=t("percentile_threshold_help")
        )

    with st.expander(t("user_settings"), expanded=False):
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>{t('email_notifications')}</p>", unsafe_allow_html=True)
        
        db = st.session_state.notifications_db
        
        st.session_state.enable_email_notifications = st.toggle(
            t("enable_email_notifications"),
            value=st.session_state.get("enable_email_notifications", False),
            help=t("enable_email_notifications_help")
        )
        
        if st.session_state.enable_email_notifications:
            st.session_state.user_email = st.text_input(
                t("destination_email"),
                value=st.session_state.get("user_email", ""),
                help=t("destination_email_help")
            )
            st.session_state.gmail_user = st.text_input(
                t("gmail_sender"),
                value=st.session_state.get("gmail_user", ""),
                help=t("gmail_sender_help")
            )
            st.session_state.gmail_app_password = st.text_input(
                t("gmail_app_password"),
                type="password",
                value=st.session_state.get("gmail_app_password", ""),
                help=t("gmail_app_password_help")
            )
            st.info(t("email_instructions"))
            
            col_save, col_clear = st.columns(2)
            with col_save:
                if st.button(t("save"), key="save_email_cfg", use_container_width=True):
                    if st.session_state.user_email and st.session_state.gmail_user:
                        success, msg = db.save_email_config(
                            st.session_state.user_email,
                            st.session_state.gmail_user,
                            st.session_state.get("gmail_app_password", "")
                        )
                        db.save_preferences(True)
                        st.toast(msg)
                    else:
                        st.toast(t("complete_all_fields"))
            with col_clear:
                if st.button(t("clear"), key="clear_email_cfg", use_container_width=True):
                    db.delete_email_config()
                    st.session_state.user_email = ""
                    st.session_state.gmail_user = ""
                    st.session_state.gmail_app_password = ""
                    st.session_state.enable_email_notifications = False
                    db.save_preferences(False)
                    st.toast(t("configuration_deleted"))
                    st.rerun()
        else:
            db.save_preferences(False)

        st.markdown("---")
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>{t('arp_filter')}</p>", unsafe_allow_html=True)
        st.session_state.arp_limit_mode = st.selectbox(
            t("arp_limit_mode"),
            options=["low", "medium", "high", "none"],
            index=["low", "medium", "high", "none"].index(
                st.session_state.get("arp_limit_mode", "medium")
            ),
            help=t("arp_limit_mode_help")
        )

    # Toggle de tema claro/oscuro
    st.divider()
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    theme_label = t("dark_mode") if is_dark else t("light_mode")
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

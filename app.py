import streamlit as st
import sklearn
from pathlib import Path
from sklearn.metrics import DistanceMetric
import sklearn.metrics._dist_metrics as _dm

# Importar del_columns para que joblib pueda deserializar los modelos
from del_columns import del_columns

# Importar AutoencoderClassifier para que joblib pueda deserializar autoencoder.pkl
# el módulo está dentro del paquete `backend`, así que usamos la ruta completa
from backend.autoencoder_classifier import AutoencoderClassifier

# Imports de backend
from backend.notifications_db import NotificationsDB
from backend.notifications import NotificationManager
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
t = get_current_theme()
c = t.colors

with st.sidebar:
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
        st.caption(f"Conectado como: {st.session_state.username}")
        if st.button("Cerrar sesión", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # ── Menú de navegación nativo (sin iframe, respeta el tema) ──
    _nav_items = [
        ("🏠 Inicio", "home"),
        ("📚 Guía del Sistema", "guia"),
        ("🛡️ Panel de Control", "dashboard"),
        ("📊 Comparar Modelos", "compare"),
    ]
    
    # Título de sección
    st.markdown(f"""
    <p style="
        font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.05em; color: {c.text_secondary};
        padding: 0.3rem 0.2rem; margin: 0 0 0.3rem 0;
    ">Navegación</p>
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

    with st.expander("⚙️ Configuración avanzada", expanded=False):
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>🤖 Autoencoder</p>", unsafe_allow_html=True)
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
        
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>🔵 OCSVM</p>", unsafe_allow_html=True)
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

    with st.expander("👤 Configuración de usuario", expanded=False):
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>📧 Notificaciones por Email</p>", unsafe_allow_html=True)
        
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
            st.session_state.gmail_app_password = st.text_input(
                "🔑 Contraseña de aplicación Gmail",
                type="password",
                value=st.session_state.get("gmail_app_password", ""),
                help="Genera en: https://myaccount.google.com/apppasswords (no es tu contraseña normal)"
            )
            st.info(
                "📌 **Instrucciones:**\n"
                "1. Ve a https://myaccount.google.com/apppasswords\n"
                "2. Asegúrate de tener verificación en 2 pasos activada\n"
                "3. Selecciona 'Mail' y 'Windows Computer'\n"
                "4. Copia la contraseña de 16 caracteres y pégala arriba"
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
        st.markdown(f"<p style='font-weight:600;color:{c.heading_secondary};margin:0.8rem 0 0.3rem 0;'>🛡️ Filtro ARP</p>", unsafe_allow_html=True)
        st.session_state.arp_limit_mode = st.selectbox(
            "Modo de límite ARP",
            options=["low", "medium", "high", "none"],
            index=["low", "medium", "high", "none"].index(
                st.session_state.get("arp_limit_mode", "medium")
            ),
            help="Controla cuántos paquetes ARP se permiten antes de alertar."
        )

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

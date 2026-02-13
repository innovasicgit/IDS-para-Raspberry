import streamlit as st
from pathlib import Path
import datetime as _dt
import base64
from backend import auth
from frontend.home_page import show_home_page


def _get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def _login_ui(_set_qp_fn=None):
    logo_path = Path(__file__).resolve().parent.parent / "img" / "logo.gif"
    gif_path = Path(__file__).resolve().parent.parent / "img" / "Fondo-Tecnologico.gif"

    gif_base64 = _get_image_base64(gif_path)

    st.markdown(f"""
        <style>
        .login-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .login-header {{
            position: relative;
            background: url('data:image/gif;base64,{gif_base64}') center center;
            background-size: cover;
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .login-header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(12, 74, 110, 0.70), rgba(16, 78, 99, 0.65));
            border-radius: 15px;
            z-index: 1;
        }}
        .login-header-content {{ position: relative; z-index: 2; }}
        .login-header h1 {{
            color: white;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .login-header p {{ color: #F0FAFE; font-size: 1.1rem; }}
        .logo-container {{
            position: absolute;
            top: 1rem; left: 1rem;
            z-index: 3;
            background: rgba(240, 250, 254, 0.88);
            padding: 0.3rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(12, 74, 110, 0.25);
            width: fit-content;
        }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 2rem; justify-content: center; }}
        .stTabs [data-baseweb="tab"] {{ font-size: 1.1rem; font-weight: 500; }}
        </style>
    """, unsafe_allow_html=True)

    col_space1, col_main, col_space2 = st.columns([0.5, 3, 0.5])
    with col_main:
        st.markdown(f"""
            <div class="login-header">
                <div class="logo-container">
                    <img src="data:image/gif;base64,{_get_image_base64(logo_path)}" width="120">
                </div>
                <div class="login-header-content" style="text-align: center; margin-top: 3rem;">
                    <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        🛡️ Sistema de Detección de Intrusiones para IoT
                    </h1>
                    <h3 style="color: #ffffff; font-weight: 300; margin-bottom: 0;">
                        Protegiendo el futuro digital con inteligencia artificial avanzada
                    </h3>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tabs = st.tabs(["🏠 Inicio", "🔑 Iniciar sesión", "👤 Crear Admin", "ℹ️ Acerca de"])

        # Inicio
        with tabs[0]:
            st.markdown("<br>", unsafe_allow_html=True)
            show_home_page()

        # Iniciar sesión
        with tabs[1]:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1], gap="large")
            with col1:
                st.markdown("### 📝 Credenciales")
                with st.form("login_form", clear_on_submit=False):
                    u = st.text_input("👤 Usuario", key="login_user", placeholder="Ingrese su nombre de usuario")
                    p = st.text_input("🔒 Contraseña", type="password", key="login_pass", placeholder="Ingrese su contraseña")
                    code = st.text_input("🔢 Código de acceso", key="login_code", max_chars=6, placeholder="6 dígitos")
                    st.markdown("<br>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("🚀 Iniciar sesión", use_container_width=True, type="primary")

                if submitted:
                    if not u or not p or not code:
                        st.error("❌ Todos los campos son obligatorios")
                    else:
                        ok, msg_or_role = auth.verify_login(u, p, code)
                        if ok:
                            # Crear sesión persistente y guardar en query params si se provee
                            try:
                                token = auth.create_session(u, msg_or_role, ttl_hours=24)
                            except Exception:
                                token = None
                            st.session_state.authenticated = True
                            st.session_state.username = u
                            page = st.session_state.get("page", "dashboard")
                            if _set_qp_fn and token:
                                _set_qp_fn({"token": token, "page": page})
                            st.success("✅ Autenticación exitosa. Redirigiendo…")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg_or_role}")

            with col2:
                st.markdown("### 🎫 Código temporal")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Generar código nuevo", use_container_width=True):
                    code, exp = auth.generate_code(ttl_seconds=300)
                    st.session_state._last_code = code
                    st.session_state._last_exp = exp
                    st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
                code, exp = auth.get_current_code()
                if code and exp:
                    remaining = int((exp - _dt.datetime.utcnow()).total_seconds())
                    remaining = max(0, remaining)
                    if remaining > 0:
                        minutes = remaining // 60
                        seconds = remaining % 60
                        st.success("✅ **Código vigente**")
                        st.code(code, language=None)
                        st.caption(f"⏱️ Expira en: **{minutes}m {seconds}s**")
                    else:
                        st.error("⏱️ El código ha expirado")
                        st.caption("Genere un nuevo código")
                else:
                    st.warning("⚠️ No hay código vigente")
                    st.caption("Genere un código para continuar")

        # Crear Admin
        with tabs[2]:
            st.markdown("<br>", unsafe_allow_html=True)
            admins = auth.get_admin_count()
            if admins == 0:
                col_form1, col_form2, col_form3 = st.columns([1, 2, 1])
                with col_form2:
                    st.success("✅ No existe ningún administrador. Cree el primero.")
                    with st.form("create_admin_form", clear_on_submit=True):
                        st.markdown("### 📋 Datos del administrador")
                        u = st.text_input("👤 Usuario Admin", placeholder="Nombre de usuario único")
                        p1 = st.text_input("🔒 Contraseña", type="password", placeholder="Mínimo 6 caracteres")
                        p2 = st.text_input("🔒 Confirmar contraseña", type="password", placeholder="Repita la contraseña")
                        st.markdown("<br>", unsafe_allow_html=True)
                        create = st.form_submit_button("✨ Crear Administrador", use_container_width=True, type="primary")
                    if create:
                        if not u or not p1 or not p2:
                            st.error("❌ Todos los campos son obligatorios")
                        elif len(p1) < 6:
                            st.error("❌ La contraseña debe tener al menos 6 caracteres")
                        elif p1 != p2:
                            st.error("❌ Las contraseñas no coinciden")
                        else:
                            ok, msg = auth.create_admin(u, p1)
                            if ok:
                                st.success(f"✅ {msg}")
                                st.balloons()
                                st.info("👉 Ahora puede iniciar sesión en la pestaña 'Iniciar sesión'")
                            else:
                                st.error(f"❌ {msg}")
            else:
                col_warn1, col_warn2, col_warn3 = st.columns([1, 2, 1])
                with col_warn2:
                    st.warning(f"⚠️ Ya existe{'n' if admins > 1 else ''} **{admins}** administrador{'es' if admins > 1 else ''}.")
                    st.info("ℹ️ Inicie sesión para gestionar usuarios desde el panel de administración.")

        # Acerca de
        with tabs[3]:
            st.markdown("<br>", unsafe_allow_html=True)
            col_info1, col_info2, col_info3 = st.columns([1, 2, 1])
            with col_info2:
                st.markdown("""
                ### 🛡️ Sistema de Autenticación

                Este sistema utiliza autenticación de doble factor para garantizar la seguridad:

                #### 🔐 Características de seguridad:
                - ✅ **Usuario y contraseña** encriptados con PBKDF2-SHA256
                - ✅ **Código temporal** de 6 dígitos con validez de 5 minutos
                - ✅ **Acceso exclusivo** para administradores
                - ✅ **Base de datos** SQLite local segura

                #### 📝 Proceso de acceso:
                1. Genere un código temporal usando el botón correspondiente
                2. El código tiene validez de **5 minutos**
                3. Ingrese usuario, contraseña y código
                4. Acceda al panel de control del IDS

                #### ⚙️ Tecnologías:
                - **Backend:** Python + SQLite
                - **Frontend:** Streamlit
                - **Seguridad:** PBKDF2, HMAC, Secrets

                ---

                **© 2026 Innovasic | UCC**
                """)
        
        # TAB: ACERCA DE
        with tabs[3]:
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_info1, col_info2, col_info3 = st.columns([1, 2, 1])
            with col_info2:
                st.markdown("""
                ### 🛡️ Sistema de Autenticación
                
                Este sistema utiliza autenticación de doble factor para garantizar la seguridad:
                
                #### 🔐 Características de seguridad:
                - ✅ **Usuario y contraseña** encriptados con PBKDF2-SHA256
                - ✅ **Código temporal** de 6 dígitos con validez de 5 minutos
                - ✅ **Acceso exclusivo** para administradores
                - ✅ **Base de datos** SQLite local segura
                
                #### 📝 Proceso de acceso:
                1. Genere un código temporal usando el botón correspondiente
                2. El código tiene validez de **5 minutos**
                3. Ingrese usuario, contraseña y código
                4. Acceda al panel de control del IDS
                
                #### ⚙️ Tecnologías:
                - **Backend:** Python + SQLite
                - **Frontend:** Streamlit
                - **Seguridad:** PBKDF2, HMAC, Secrets
                
                ---
                
                **© 2026 Innovasic | UCC**
                """)


def ensure_auth():
    """
    Asegura que el usuario esté autenticado.
    Si no lo está, muestra la interfaz de login y detiene la ejecución.
    """
    if not st.session_state.get("authenticated", False):
        _login_ui()
        st.stop()

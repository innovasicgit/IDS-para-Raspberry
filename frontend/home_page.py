"""
Página de inicio del Sistema IDS para IoT.
Página principal con información del sistema, características y guía de uso.
Diseño profesional UI/UX con glassmorphism y gradientes creativos.
"""

import streamlit as st


def show_home_page():
    """Mostrar página de inicio con información del sistema."""

    # Título principal con gradient y glow
    st.markdown("""
    <div style="padding: 40px 30px; background: linear-gradient(135deg, #0C4A6E 0%, #1383A7 50%, #104E63 100%); 
                border-radius: 20px; color: white; text-align: center; margin: 20px 0;
                box-shadow: 0 10px 40px rgba(19,131,167,0.2), 0 0 60px rgba(19,131,167,0.08);
                position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                    background: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.05) 0%, transparent 50%);
                    pointer-events: none;"></div>
        <h1 style="margin: 0; color: white; font-size: 2.5rem; position: relative; z-index: 1;
                   text-shadow: 0 2px 10px rgba(0,0,0,0.2);">🛡️ Sistema de Detección de Intrusos</h1>
        <p style="margin: 15px 0 0 0; font-size: 1.2em; color: rgba(240,250,254,0.9); position: relative; z-index: 1;">
            Monitoreo de red en tiempo real con Inteligencia Artificial</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de características principales con difuminado
    st.markdown("<br>", unsafe_allow_html=True)
    col_feat1, col_feat2, col_feat3 = st.columns(3, gap="medium")
    with col_feat1:
        st.markdown("""
        <div style="text-align: center; padding: 30px; 
                    background: linear-gradient(160deg, rgba(28,168,212,0.12) 0%, rgba(19,131,167,0.05) 100%);
                    border-radius: 16px; height: 200px; display: flex; flex-direction: column; justify-content: center;
                    border: 1px solid rgba(19,131,167,0.15);
                    box-shadow: 0 4px 20px rgba(19,131,167,0.08);
                    transition: all 0.3s ease;">
            <div style="font-size: 3em; margin-bottom: 8px;">⚡</div>
            <p style="margin: 8px 0 5px 0; font-size: 1.2em; color: #F0FAFE;"><strong>Tiempo Real</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 0.95em; color: rgba(240,250,254,0.55);">Captura y análisis instantáneo</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; 
                    background: linear-gradient(160deg, rgba(16,185,129,0.12) 0%, rgba(16,185,129,0.04) 100%);
                    border-radius: 16px; height: 200px; display: flex; flex-direction: column; justify-content: center;
                    border: 1px solid rgba(16,185,129,0.15);
                    box-shadow: 0 4px 20px rgba(16,185,129,0.06);
                    transition: all 0.3s ease;">
            <div style="font-size: 3em; margin-bottom: 8px;">🤖</div>
            <p style="margin: 8px 0 5px 0; font-size: 1.2em; color: #F0FAFE;"><strong>IA Avanzada</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 0.95em; color: rgba(240,250,254,0.55);">4 modelos de Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat3:
        st.markdown("""
        <div style="text-align: center; padding: 30px; 
                    background: linear-gradient(160deg, rgba(245,158,11,0.12) 0%, rgba(245,158,11,0.04) 100%);
                    border-radius: 16px; height: 200px; display: flex; flex-direction: column; justify-content: center;
                    border: 1px solid rgba(245,158,11,0.12);
                    box-shadow: 0 4px 20px rgba(245,158,11,0.06);
                    transition: all 0.3s ease;">
            <div style="font-size: 3em; margin-bottom: 8px;">📊</div>
            <p style="margin: 8px 0 5px 0; font-size: 1.2em; color: #F0FAFE;"><strong>Visualización</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 0.95em; color: rgba(240,250,254,0.55);">Gráficas interactivas y reportes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Descripción principal con glassmorphism
    st.markdown("""
    <div style="background: linear-gradient(160deg, rgba(19,131,167,0.10) 0%, rgba(12,74,110,0.05) 100%); 
                padding: 2rem; border-radius: 16px; 
                border-left: 4px solid #1383A7; margin: 2rem 0;
                backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <p style="font-size: 1.15rem; line-height: 1.8; text-align: justify; color: rgba(240,250,254,0.85);">
            Bienvenido al <strong style="color: #1CA8D4;">Sistema de Detección de Intrusiones en Redes IoT</strong>, 
            una solución avanzada diseñada para monitorear y detectar anomalías 
            en redes de IoT, brindando seguridad y confiabilidad sin precedentes.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify; margin-top: 1rem; color: rgba(240,250,254,0.7);">
            Nuestro sistema utiliza modelos de vanguardia en detección de anomalías, como 
            <strong style="color: #10B981;">IForest</strong>, <strong style="color: #F59E0B;">OCSVM</strong>,
            <strong style="color: #1383A7;">K-MEANS</strong> y <strong style="color: #EF4444;">Autoencoder multiclase</strong> 
            para analizar patrones complejos y alertar sobre posibles irregularidades en la red en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de ingreso
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("�� Ingresar al Sistema", use_container_width=True, type="primary", key="btn_top"):
            st.session_state.page = "dashboard"
            st.rerun()

    # Características Principales
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1CA8D4; margin: 2.5rem 0 2rem 0; font-weight: 600;">
        🎯 Características Principales del Sistema
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(180deg, rgba(16,185,129,0.12) 0%, rgba(16,185,129,0.03) 100%); 
                    padding: 1.5rem; border-radius: 16px; text-align: center; height: 280px; 
                    border: 1px solid rgba(16,185,129,0.18); box-shadow: 0 4px 15px rgba(16,185,129,0.05);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #10B981; margin-bottom: 0.8rem; font-size: 1.05rem;">Detección en Tiempo Real</h3>
            <p style="font-size: 0.9rem; line-height: 1.6; color: rgba(240,250,254,0.6);">
                Monitoreo continuo y análisis instantáneo de patrones de red
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(180deg, rgba(19,131,167,0.12) 0%, rgba(19,131,167,0.03) 100%); 
                    padding: 1.5rem; border-radius: 16px; text-align: center; height: 280px; 
                    border: 1px solid rgba(19,131,167,0.18); box-shadow: 0 4px 15px rgba(19,131,167,0.05);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #1383A7; margin-bottom: 0.8rem; font-size: 1.05rem;">IA Avanzada</h3>
            <p style="font-size: 0.9rem; line-height: 1.6; color: rgba(240,250,254,0.6);">
                Algoritmos de machine learning de última generación
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(180deg, rgba(245,158,11,0.12) 0%, rgba(245,158,11,0.03) 100%); 
                    padding: 1.5rem; border-radius: 16px; text-align: center; height: 280px; 
                    border: 1px solid rgba(245,158,11,0.15); box-shadow: 0 4px 15px rgba(245,158,11,0.05);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #F59E0B; margin-bottom: 0.8rem; font-size: 1.05rem;">Análisis Predictivo</h3>
            <p style="font-size: 0.9rem; line-height: 1.6; color: rgba(240,250,254,0.6);">
                Predicción de amenazas y comportamientos anómalos
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(180deg, rgba(239,68,68,0.12) 0%, rgba(239,68,68,0.03) 100%); 
                    padding: 1.5rem; border-radius: 16px; text-align: center; height: 280px; 
                    border: 1px solid rgba(239,68,68,0.15); box-shadow: 0 4px 15px rgba(239,68,68,0.05);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚫</div>
            <h3 style="color: #EF4444; margin-bottom: 0.8rem; font-size: 1.05rem;">Protección Activa</h3>
            <p style="font-size: 0.9rem; line-height: 1.6; color: rgba(240,250,254,0.6);">
                Identificación y mitigación automática de amenazas
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Interpretación de Resultados
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1CA8D4; margin: 2.5rem 0 2rem 0; font-weight: 600;">
        💬 Interpretación de Resultados
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(16,185,129,0.10) 0%, rgba(16,185,129,0.03) 100%); 
                    padding: 1.5rem; border-radius: 14px; border-left: 4px solid #10B981;
                    box-shadow: 0 4px 15px rgba(16,185,129,0.05);">
            <h3 style="color: #10B981; margin-bottom: 1rem; font-size: 1.05rem;">🟢 Métricas de Validación</h3>
            <ul style="line-height: 2; color: rgba(240,250,254,0.75); font-size: 0.92rem;">
                <li><strong style="color: #F0FAFE;">Silhouette Score:</strong> Calidad de clusters (ideal > 0.5)</li>
                <li><strong style="color: #F0FAFE;">Calinski Score:</strong> Separación entre clusters</li>
                <li><strong style="color: #F0FAFE;">Davies Score:</strong> Similitud dentro de clusters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(19,131,167,0.10) 0%, rgba(19,131,167,0.03) 100%); 
                    padding: 1.5rem; border-radius: 14px; border-left: 4px solid #1383A7;
                    box-shadow: 0 4px 15px rgba(19,131,167,0.05);">
            <h3 style="color: #1383A7; margin-bottom: 1rem; font-size: 1.05rem;">🔰 Clasificación de Anomalías</h3>
            <ul style="line-height: 2; color: rgba(240,250,254,0.75); font-size: 0.92rem;">
                <li><strong style="color: #F0FAFE;">Normal:</strong> Tráfico de red esperado</li>
                <li><strong style="color: #F0FAFE;">Anómalo:</strong> Patrones sospechosos</li>
                <li><strong style="color: #F0FAFE;">Multiclase:</strong>
                    <ul><li>DDoS_TCP · DDoS_UDP · Reconnaissance</li></ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(245,158,11,0.10) 0%, rgba(245,158,11,0.03) 100%); 
                    padding: 1.5rem; border-radius: 14px; border-left: 4px solid #F59E0B;
                    box-shadow: 0 4px 15px rgba(245,158,11,0.05);">
            <h3 style="color: #F59E0B; margin-bottom: 1rem; font-size: 1.05rem;">⚡ Métricas de Rendimiento</h3>
            <ul style="line-height: 2; color: rgba(240,250,254,0.75); font-size: 0.92rem;">
                <li><strong style="color: #F0FAFE;">CPU:</strong> % Consumo por segundo</li>
                <li><strong style="color: #F0FAFE;">Memoria:</strong> % Uso de RAM</li>
                <li><strong style="color: #F0FAFE;">Disco:</strong> % Uso de almacenamiento</li>
                <li><strong style="color: #F0FAFE;">Tiempo:</strong> Duración en segundos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Modelos de Detección
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1CA8D4; margin: 2.5rem 0 2rem 0; font-weight: 600;">
        🔎 Modelos de Detección de Anomalías
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(19,131,167,0.12) 0%, rgba(19,131,167,0.04) 100%); 
                    padding: 1.5rem; border-radius: 14px; margin-bottom: 1rem; 
                    border: 1px solid rgba(19,131,167,0.20); box-shadow: 0 4px 15px rgba(19,131,167,0.06);">
            <h3 style="color: #1383A7; font-size: 1.05rem;">🔵 OCSVM (One Class SVM)</h3>
            <p style="line-height: 1.8; margin-top: 0.8rem; color: rgba(240,250,254,0.7); font-size: 0.95rem;">
                Modelo que aprende características del tráfico normal y detecta desviaciones. 
                Ideal para escenarios donde solo se tiene acceso a datos normales.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(16,185,129,0.12) 0%, rgba(16,185,129,0.04) 100%); 
                    padding: 1.5rem; border-radius: 14px; margin-bottom: 1rem; 
                    border: 1px solid rgba(16,185,129,0.20); box-shadow: 0 4px 15px rgba(16,185,129,0.06);">
            <h3 style="color: #10B981; font-size: 1.05rem;">🟢 IForest (Isolation Forest)</h3>
            <p style="line-height: 1.8; margin-top: 0.8rem; color: rgba(240,250,254,0.7); font-size: 0.95rem;">
                Algoritmo basado en árboles que aísla anomalías de forma eficiente. 
                Excelente para detectar outliers en grandes volúmenes de datos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(245,158,11,0.12) 0%, rgba(245,158,11,0.04) 100%); 
                    padding: 1.5rem; border-radius: 14px; margin-bottom: 1rem; 
                    border: 1px solid rgba(245,158,11,0.18); box-shadow: 0 4px 15px rgba(245,158,11,0.06);">
            <h3 style="color: #F59E0B; font-size: 1.05rem;">🟠 K-means</h3>
            <p style="line-height: 1.8; margin-top: 0.8rem; color: rgba(240,250,254,0.7); font-size: 0.95rem;">
                Algoritmo de clustering no supervisado que agrupa datos similares. 
                Identifica patrones anómalos al detectar puntos alejados de los centroides.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(160deg, rgba(239,68,68,0.12) 0%, rgba(239,68,68,0.04) 100%); 
                    padding: 1.5rem; border-radius: 14px; margin-bottom: 1rem; 
                    border: 1px solid rgba(239,68,68,0.18); box-shadow: 0 4px 15px rgba(239,68,68,0.06);">
            <h3 style="color: #EF4444; font-size: 1.05rem;">🔴 Autoencoder multiclase</h3>
            <p style="line-height: 1.8; margin-top: 0.8rem; color: rgba(240,250,254,0.7); font-size: 0.95rem;">
                Red neuronal profunda que aprende representaciones comprimidas. 
                Detecta anomalías y clasifica múltiples tipos de ataques simultáneamente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Guía de Uso
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1CA8D4; margin: 2.5rem 0 2rem 0; font-weight: 600;">
        📖 Guía de Uso del Sistema
    </h2>
    """, unsafe_allow_html=True)

    steps = [
        ("🔌", "Paso 1: Seleccionar Modelo", "Elige el algoritmo de detección más adecuado"),
        ("📡", "Paso 2: Capturar Paquetes", "Inicia la captura de tráfico de red"),
        ("🖱️", "Paso 3: Realizar Predicción", "Ejecuta el análisis con un solo clic"),
        ("📊", "Paso 4: Visualizar Resultados", "Examina gráficos interactivos y métricas"),
        ("💾", "Paso 5: Guardar Resultados", "Exporta los datos en formato CSV")
    ]

    # Colores degradados para cada paso
    step_colors = ['19,131,167', '16,185,129', '245,158,11', '28,168,212', '16,78,99']

    cols = st.columns(5)
    for idx, (icon, title, desc) in enumerate(steps):
        sc = step_colors[idx]
        with cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(180deg, rgba({sc},0.12) 0%, rgba({sc},0.03) 100%); 
                        padding: 1.2rem; border-radius: 14px; text-align: center; height: 200px;
                        border: 1px solid rgba({sc},0.15); 
                        display: flex; flex-direction: column; justify-content: center;
                        box-shadow: 0 4px 15px rgba({sc},0.05);">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="color: #1CA8D4; font-size: 0.85rem; margin-bottom: 0.5rem;">{title}</h4>
                <p style="font-size: 0.8rem; line-height: 1.4; color: rgba(240,250,254,0.55);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Tipos de Resultados y Recomendaciones
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1CA8D4; margin: 2.5rem 0 2rem 0; font-weight: 600;">
        📊 Tipos de Resultados y Recomendaciones
    </h2>
    """, unsafe_allow_html=True)

    # Resultados Normales
    st.markdown("""
    <div style="background: linear-gradient(160deg, rgba(16,185,129,0.10) 0%, rgba(16,185,129,0.03) 100%); 
                padding: 2rem; border-radius: 14px; margin-bottom: 1.5rem; border-left: 4px solid #10B981;
                box-shadow: 0 4px 15px rgba(16,185,129,0.05);">
        <h3 style="color: #10B981; margin-bottom: 1rem;">✅ Resultados Normales</h3>
        <p style="font-size: 1.05rem; line-height: 1.8; color: rgba(240,250,254,0.75);">
            Los datos han sido clasificados como normales. No se han detectado anomalías 
            significativas en el tráfico de red analizado.
        </p>
        <div style="background: rgba(16,185,129,0.12); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <strong style="color: #10B981;">💡 Recomendación:</strong><br>
            <span style="color: rgba(240,250,254,0.7);">Continúa monitoreando la red regularmente para mantener la seguridad.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resultados Anómalos
    st.markdown("""
    <div style="background: linear-gradient(160deg, rgba(245,158,11,0.10) 0%, rgba(245,158,11,0.03) 100%); 
                padding: 2rem; border-radius: 14px; margin-bottom: 1.5rem; border-left: 4px solid #F59E0B;
                box-shadow: 0 4px 15px rgba(245,158,11,0.05);">
        <h3 style="color: #F59E0B; margin-bottom: 1rem;">⚠️ Resultados Anómalos</h3>
        <p style="font-size: 1.05rem; line-height: 1.8; color: rgba(240,250,254,0.75);">
            Se han detectado patrones anómalos en la red. Esto puede indicar posibles amenazas 
            o comportamientos inusuales que requieren atención.
        </p>
        <div style="background: rgba(245,158,11,0.12); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <strong style="color: #F59E0B;">🔍 Recomendación:</strong><br>
            <span style="color: rgba(240,250,254,0.7);">Investiga las anomalías detectadas y toma medidas preventivas inmediatas.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ataques Específicos
    st.markdown("""
    <div style="background: linear-gradient(160deg, rgba(239,68,68,0.10) 0%, rgba(239,68,68,0.03) 100%); 
                padding: 2rem; border-radius: 14px; margin-bottom: 1.5rem; border-left: 4px solid #EF4444;
                box-shadow: 0 4px 15px rgba(239,68,68,0.05);">
        <h3 style="color: #EF4444; margin-bottom: 1.5rem;">🚨 Ataques Específicos</h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: rgba(239,68,68,0.08); padding: 1.5rem; border-radius: 12px;
                    border: 1px solid rgba(239,68,68,0.15);">
            <h4 style="color: #EF4444; margin-bottom: 1rem;">🔴 DDoS_TCP:</h4>
            <ul style="line-height: 2; color: rgba(240,250,254,0.7); font-size: 0.92rem;">
                <li>Activa SYN cookies</li>
                <li>Configura límites de tasa</li>
                <li>Usa ACL para bloquear IPs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(245,158,11,0.08); padding: 1.5rem; border-radius: 12px;
                    border: 1px solid rgba(245,158,11,0.15);">
            <h4 style="color: #F59E0B; margin-bottom: 1rem;">🟠 DDoS_UDP:</h4>
            <ul style="line-height: 2; color: rgba(240,250,254,0.7); font-size: 0.92rem;">
                <li>Permite solo puertos necesarios</li>
                <li>Aplica límites de tasa UDP</li>
                <li>Usa null routing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: rgba(19,131,167,0.08); padding: 1.5rem; border-radius: 12px;
                    border: 1px solid rgba(19,131,167,0.15);">
            <h4 style="color: #1383A7; margin-bottom: 1rem;">🔵 Reconnaissance:</h4>
            <ul style="line-height: 2; color: rgba(240,250,254,0.7); font-size: 0.92rem;">
                <li>Restringe respuestas ICMP</li>
                <li>Expón solo puertos necesarios</li>
                <li>Configura límites anti-scan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Call to Action Final
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem 1rem 2rem; 
                background: linear-gradient(135deg, #0C4A6E 0%, #104E63 50%, #0C1B2E 100%); 
                border-radius: 20px; margin: 2rem 0;
                box-shadow: 0 10px 40px rgba(12,74,110,0.2);
                position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                    background: radial-gradient(circle at 50% 30%, rgba(19,131,167,0.15) 0%, transparent 60%);
                    pointer-events: none;"></div>
        <h2 style="color: #F0FAFE; margin-bottom: 1rem; font-size: 2rem; position: relative; z-index: 1;">
            ¿Listo para comenzar?
        </h2>
        <p style="color: rgba(240,250,254,0.7); font-size: 1.15rem; margin-bottom: 1.5rem; position: relative; z-index: 1;">
            Inicia sesión para acceder al <strong style="color: #1CA8D4;">Panel de Control</strong> y empezar a proteger tu red IoT
        </p>
        <div style="font-size: 3rem; margin-bottom: 1.5rem; position: relative; z-index: 1;">🚀</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Ingresar al Sistema", use_container_width=True, type="primary", key="btn_bottom"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(240,250,254,0.3);">
        <p style="margin: 0;">🛡️ Sistema de Detección de Anomalías IoT</p>
        <p style="margin: 0.5rem 0 0 0;">© 2026 Innovasic | UCC</p>
    </div>
    """, unsafe_allow_html=True)

"""
Página de inicio del Sistema IDS para IoT.
Página principal con información del sistema, características y guía de uso.
"""

import streamlit as st


def show_home_page():
    """Mostrar página de inicio con información del sistema."""

    # Descripción principal
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 2rem; border-radius: 15px; 
                border-left: 4px solid #4CAF50; margin: 2rem 0;">
        <p style="font-size: 1.2rem; line-height: 1.8; text-align: justify;">
            Bienvenido al <strong>Sistema de Detección de Intrusiones en Redes IoT</strong>, 
            una solución avanzada diseñada para monitorear y detectar anomalías 
            en redes de IoT, brindando seguridad y confiabilidad sin precedentes.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1rem;">
            Nuestro sistema utiliza modelos de vanguardia en detección de anomalías, como 
            <strong>IForest</strong> (Isolation Forest), <strong>OCSVM</strong> (One Class Support Vector Machine),
            <strong>K-MEANS</strong> y <strong>Autoencoder multiclase</strong> para analizar patrones complejos 
            y alertar sobre posibles irregularidades en la red en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de ingreso después de la descripción
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Ingresar al Sistema", use_container_width=True, type="primary", key="btn_top"):
            st.session_state.page = "dashboard"
            st.rerun()

    # Características Principales
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
        🎯 Características Principales del Sistema
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(76, 175, 80, 0.3);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #4CAF50; margin-bottom: 1rem;">Detección en Tiempo Real</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Monitoreo continuo y análisis instantáneo de patrones de red
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(66, 165, 245, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(66, 165, 245, 0.3);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #42A5F5; margin-bottom: 1rem;">IA Avanzada</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Algoritmos de machine learning de última generación
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 167, 38, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(255, 167, 38, 0.3);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #FFA726; margin-bottom: 1rem;">Análisis Predictivo</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Predicción de amenazas y comportamientos anómalos
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: rgba(255, 82, 82, 0.1); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(255, 82, 82, 0.3);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🚫</div>
            <h3 style="color: #FF5252; margin-bottom: 1rem;">Protección Activa</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Identificación y mitigación automática de amenazas
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Interpretación de Resultados
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
        💬 Interpretación de Resultados
    </h2>
    """, unsafe_allow_html=True)

    # Tres columnas para métricas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.1); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #4CAF50;">
            <h3 style="color: #4CAF50; margin-bottom: 1rem;">🟢 Métricas de Validación</h3>
            <ul style="line-height: 2;">
                <li><strong>Silhouette Score:</strong> Mide la calidad de los clusters (ideal > 0.5)</li>
                <li><strong>Calinski Score:</strong> Evalúa la separación entre clusters</li>
                <li><strong>Davies Score:</strong> Indica la similitud dentro de clusters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(66, 165, 245, 0.1); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #42A5F5;">
            <h3 style="color: #42A5F5; margin-bottom: 1rem;">🔰 Clasificación de Anomalías</h3>
            <ul style="line-height: 2;">
                <li><strong>Normal:</strong> Tráfico de red esperado</li>
                <li><strong>Anómalo:</strong> Patrones sospechosos</li>
                <li><strong>Multiclase:</strong>
                    <ul>
                        <li>DDoS_TCP</li>
                        <li>DDoS_UDP</li>
                        <li>Reconnaissance</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: rgba(255, 167, 38, 0.1); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #FFA726;">
            <h3 style="color: #FFA726; margin-bottom: 1rem;">📈 Métricas de Rendimiento</h3>
            <ul style="line-height: 2;">
                <li><strong>CPU:</strong> % Consumo por segundo</li>
                <li><strong>Memoria:</strong> % Uso de RAM</li>
                <li><strong>Disco:</strong> % Uso de almacenamiento</li>
                <li><strong>Tiempo:</strong> Duración en segundos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Modelos de Detección
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
        🔎 Modelos de Detección de Anomalías
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: rgba(66, 165, 245, 0.1); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #42A5F5;">
            <h3 style="color: #42A5F5;">🔵 OCSVM (One Class Support Vector Machine)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Modelo de aprendizaje supervisado que aprende características del tráfico normal 
                y detecta desviaciones. Ideal para escenarios donde solo se tiene acceso a datos normales.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(76, 175, 80, 0.1); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #4CAF50;">
            <h3 style="color: #4CAF50;">🟢 IForest (Isolation Forest)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Algoritmo basado en árboles de decisión que aísla anomalías de forma eficiente. 
                Excelente para detectar outliers en grandes volúmenes de datos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(255, 167, 38, 0.1); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #FFA726;">
            <h3 style="color: #FFA726;">🟠 K-means</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Algoritmo de clustering no supervisado que agrupa datos similares. 
                Identifica patrones anómalos al detectar puntos alejados de los centroides.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(255, 82, 82, 0.1); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #FF5252;">
            <h3 style="color: #FF5252;">🔴 Autoencoder multiclase</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Red neuronal profunda que aprende representaciones comprimidas de datos normales. 
                Detecta anomalías y clasifica múltiples tipos de ataques simultáneamente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Guía de Uso
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
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

    cols = st.columns(5)
    for idx, (icon, title, desc) in enumerate(steps):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: rgba(66, 165, 245, 0.1); padding: 1rem; 
                        border-radius: 12px; text-align: center; height: 200px;
                        border: 1px solid rgba(66, 165, 245, 0.3);">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="color: #42A5F5; font-size: 0.9rem; margin-bottom: 0.5rem;">{title}</h4>
                <p style="font-size: 0.85rem; line-height: 1.4;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Tipos de Resultados y Recomendaciones
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #4CAF50; margin: 3rem 0 2rem 0;">
        📊 Tipos de Resultados y Recomendaciones
    </h2>
    """, unsafe_allow_html=True)

    # Resultados Normales
    st.markdown("""
    <div style="background: rgba(76, 175, 80, 0.1); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #4CAF50;">
        <h3 style="color: #4CAF50; margin-bottom: 1rem;">
            ✅ Resultados Normales
        </h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Los datos han sido clasificados como normales. No se han detectado anomalías 
            significativas en el tráfico de red analizado.
        </p>
        <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #4CAF50;">💡 Recomendación:</strong><br>
            Continúa monitoreando la red regularmente para mantener la seguridad.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resultados Anómalos
    st.markdown("""
    <div style="background: rgba(255, 167, 38, 0.1); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #FFA726;">
        <h3 style="color: #FFA726; margin-bottom: 1rem;">
            ⚠️ Resultados Anómalos
        </h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Se han detectado patrones anómalos en la red. Esto puede indicar posibles amenazas 
            o comportamientos inusuales que requieren atención.
        </p>
        <div style="background: rgba(255, 167, 38, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #FFA726;">🔍 Recomendación:</strong><br>
            Investiga las anomalías detectadas y toma medidas preventivas inmediatas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ataques Específicos
    st.markdown("""
    <div style="background: rgba(255, 82, 82, 0.1); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #FF5252;">
        <h3 style="color: #FF5252; margin-bottom: 1.5rem;">
            🚨 Ataques Específicos
        </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: rgba(255, 82, 82, 0.15); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #FF5252; margin-bottom: 1rem;">🔴 DDoS_TCP:</h4>
            <ul style="line-height: 2;">
                <li>Activa SYN cookies</li>
                <li>Configura límites de tasa</li>
                <li>Usa ACL para bloquear IPs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(255, 167, 38, 0.15); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #FFA726; margin-bottom: 1rem;">🟠 DDoS_UDP:</h4>
            <ul style="line-height: 2;">
                <li>Permite solo puertos necesarios</li>
                <li>Aplica límites de tasa UDP</li>
                <li>Usa null routing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: rgba(66, 165, 245, 0.15); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #42A5F5; margin-bottom: 1rem;">🔵 Reconnaissance:</h4>
            <ul style="line-height: 2;">
                <li>Restringe respuestas ICMP</li>
                <li>Expón solo puertos necesarios</li>
                <li>Configura límites anti-scan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Call to Action Final con botón integrado
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem 1rem 2rem; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 1rem; font-size: 2rem;">
            ¿Listo para comenzar?
        </h2>
        <p style="color: white; font-size: 1.2rem; margin-bottom: 1.5rem;">
            Inicia sesión para acceder al <strong>Panel de Control</strong> y empezar a proteger tu red IoT
        </p>
        <div style="font-size: 3rem; margin-bottom: 1.5rem;">🚀</div>
    """, unsafe_allow_html=True)
    
    # Botón dentro del mismo contenedor verde
    st.markdown("<style>.stButton > button {font-size: 1.5rem !important; padding: 1rem 3rem !important; font-weight: bold !important;}</style>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Ingresar al Sistema", use_container_width=True, type="primary", key="btn_bottom"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(255,255,255,0.5);">
        <p style="margin: 0;">🛡️ Sistema de Detección de Anomalías IoT</p>
        <p style="margin: 0.5rem 0 0 0;">© 2026 Innovasic | UCC</p>
    </div>
    """, unsafe_allow_html=True)

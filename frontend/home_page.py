"""
Página de inicio del Sistema IDS para IoT.
Página principal con información del sistema, características y guía de uso.
"""

import streamlit as st


def show_home_page():
    """Mostrar página de inicio con información del sistema."""

    # URLs de imágenes estáticas (servidas por Streamlit static serving)
    img2_url = "app/static/img2.jpg"
    img4_url = "app/static/img4.png"

    # Título principal con imagen de fondo (static serving)
    st.markdown(f"""
    <style>
        .home-hero {{
            position: relative;
            padding: 50px 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 20px 0;
            overflow: hidden;
            background: url('{img2_url}') center center / cover no-repeat;
        }}
        .home-hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            z-index: 1;
        }}
        .home-hero-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="home-hero">
        <div class="home-hero-content">
            <h1 style="margin: 0; color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">🛡️ Sistema de Detección de Intrusos</h1>
            <p style="margin: 15px 0 0 0; font-size: 1.2em; color: #F0FAFE; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">Monitoreo de red en tiempo real con Inteligencia Artificial</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de características principales
    st.markdown("<br>", unsafe_allow_html=True)
    col_feat1, col_feat2, col_feat3 = st.columns(3, gap="medium")
    with col_feat1:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: rgba(19, 131, 167, 0.08); border-radius: 15px; height: 200px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(19, 131, 167, 0.2);">
            <h1 style="margin: 0; font-size: 3em;">⚡</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>Tiempo Real</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: rgba(240, 250, 254, 0.7);">Captura y análisis instantáneo</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: rgba(19, 131, 167, 0.08); border-radius: 15px; height: 200px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(19, 131, 167, 0.2);">
            <h1 style="margin: 0; font-size: 3em;">🤖</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>IA Avanzada</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: rgba(240, 250, 254, 0.7);">4 modelos de Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat3:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: rgba(19, 131, 167, 0.08); border-radius: 15px; height: 200px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(19, 131, 167, 0.2);">
            <h1 style="margin: 0; font-size: 3em;">📊</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>Visualización</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: rgba(240, 250, 254, 0.7);">Gráficas interactivas y reportes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Descripción principal
    st.markdown("""
    <div style="background: rgba(19, 131, 167, 0.06); padding: 2rem; border-radius: 15px; 
                border-left: 4px solid #1383A7; margin: 2rem 0;">
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

    # Características Principales
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1383A7; margin: 3rem 0 2rem 0;">
        🎯 Características Principales del Sistema
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(16, 185, 129, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #10B981; margin-bottom: 1rem;">Detección en Tiempo Real</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Monitoreo continuo y análisis instantáneo de patrones de red
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(19, 131, 167, 0.08); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(19, 131, 167, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #1383A7; margin-bottom: 1rem;">IA Avanzada</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Algoritmos de machine learning de última generación
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.08); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(245, 158, 11, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #F59E0B; margin-bottom: 1rem;">Análisis Predictivo</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Predicción de amenazas y comportamientos anómalos
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.08); padding: 1.5rem; 
                    border-radius: 15px; text-align: center; height: 280px; 
                    border: 1px solid rgba(239, 68, 68, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🚫</div>
            <h3 style="color: #EF4444; margin-bottom: 1rem;">Protección Activa</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">
                Identificación y mitigación automática de amenazas
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Interpretación de Resultados
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1383A7; margin: 3rem 0 2rem 0;">
        💬 Interpretación de Resultados
    </h2>
    """, unsafe_allow_html=True)

    # Tres columnas para métricas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #10B981;">
            <h3 style="color: #10B981; margin-bottom: 1rem;">🟢 Métricas de Validación</h3>
            <ul style="line-height: 2;">
                <li><strong>Silhouette Score:</strong> Mide la calidad de los clusters (ideal > 0.5)</li>
                <li><strong>Calinski Score:</strong> Evalúa la separación entre clusters</li>
                <li><strong>Davies Score:</strong> Indica la similitud dentro de clusters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(19, 131, 167, 0.08); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #1383A7;">
            <h3 style="color: #1383A7; margin-bottom: 1rem;">🔰 Clasificación de Anomalías</h3>
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
        <div style="background: rgba(245, 158, 11, 0.08); padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid #F59E0B;">
            <h3 style="color: #F59E0B; margin-bottom: 1rem;">�� Métricas de Rendimiento</h3>
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
    <h2 style="text-align: center; color: #1383A7; margin: 3rem 0 2rem 0;">
        🔎 Modelos de Detección de Anomalías
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: rgba(19, 131, 167, 0.08); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #1383A7;">
            <h3 style="color: #1383A7;">🔵 OCSVM (One Class Support Vector Machine)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Modelo de aprendizaje supervisado que aprende características del tráfico normal 
                y detecta desviaciones. Ideal para escenarios donde solo se tiene acceso a datos normales.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #10B981;">
            <h3 style="color: #10B981;">🟢 IForest (Isolation Forest)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Algoritmo basado en árboles de decisión que aísla anomalías de forma eficiente. 
                Excelente para detectar outliers en grandes volúmenes de datos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.08); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #F59E0B;">
            <h3 style="color: #F59E0B;">🟠 K-means</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Algoritmo de clustering no supervisado que agrupa datos similares. 
                Identifica patrones anómalos al detectar puntos alejados de los centroides.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.08); padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid #EF4444;">
            <h3 style="color: #EF4444;">🔴 Autoencoder multiclase</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                Red neuronal profunda que aprende representaciones comprimidas de datos normales. 
                Detecta anomalías y clasifica múltiples tipos de ataques simultáneamente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Guía de Uso
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1383A7; margin: 3rem 0 2rem 0;">
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
            <div style="background: rgba(19, 131, 167, 0.08); padding: 1rem; 
                        border-radius: 12px; text-align: center; height: 200px;
                        border: 1px solid rgba(19, 131, 167, 0.25);">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="color: #1383A7; font-size: 0.9rem; margin-bottom: 0.5rem;">{title}</h4>
                <p style="font-size: 0.85rem; line-height: 1.4;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Tipos de Resultados y Recomendaciones
    st.markdown("---")
    st.markdown("""
    <h2 style="text-align: center; color: #1383A7; margin: 3rem 0 2rem 0;">
        📊 Tipos de Resultados y Recomendaciones
    </h2>
    """, unsafe_allow_html=True)

    # Resultados Normales
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.08); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #10B981;">
        <h3 style="color: #10B981; margin-bottom: 1rem;">
            ✅ Resultados Normales
        </h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Los datos han sido clasificados como normales. No se han detectado anomalías 
            significativas en el tráfico de red analizado.
        </p>
        <div style="background: rgba(16, 185, 129, 0.15); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #10B981;">💡 Recomendación:</strong><br>
            Continúa monitoreando la red regularmente para mantener la seguridad.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resultados Anómalos
    st.markdown("""
    <div style="background: rgba(245, 158, 11, 0.08); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #F59E0B;">
        <h3 style="color: #F59E0B; margin-bottom: 1rem;">
            ⚠️ Resultados Anómalos
        </h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Se han detectado patrones anómalos en la red. Esto puede indicar posibles amenazas 
            o comportamientos inusuales que requieren atención.
        </p>
        <div style="background: rgba(245, 158, 11, 0.15); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong style="color: #F59E0B;">🔍 Recomendación:</strong><br>
            Investiga las anomalías detectadas y toma medidas preventivas inmediatas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ataques Específicos
    st.markdown("""
    <div style="background: rgba(239, 68, 68, 0.08); padding: 2rem; border-radius: 12px; 
                margin-bottom: 1.5rem; border-left: 5px solid #EF4444;">
        <h3 style="color: #EF4444; margin-bottom: 1.5rem;">
            🚨 Ataques Específicos
        </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.12); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #EF4444; margin-bottom: 1rem;">🔴 DDoS_TCP:</h4>
            <ul style="line-height: 2;">
                <li>Activa SYN cookies</li>
                <li>Configura límites de tasa</li>
                <li>Usa ACL para bloquear IPs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.12); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #F59E0B; margin-bottom: 1rem;">🟠 DDoS_UDP:</h4>
            <ul style="line-height: 2;">
                <li>Permite solo puertos necesarios</li>
                <li>Aplica límites de tasa UDP</li>
                <li>Usa null routing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: rgba(19, 131, 167, 0.12); padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #1383A7; margin-bottom: 1rem;">🔵 Reconnaissance:</h4>
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
    st.markdown(f"""
    <style>
        .home-cta {{
            position: relative;
            text-align: center;
            padding: 3rem 2rem 1rem 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            overflow: hidden;
            background: url('{img4_url}') center center / cover no-repeat;
        }}
        .home-cta::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            z-index: 1;
        }}
        .home-cta-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="home-cta">
        <div class="home-cta-content">
            <h2 style="color: #F0FAFE; margin-bottom: 1rem; font-size: 2rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">
                ¿Listo para comenzar?
            </h2>
            <p style="color: rgba(240, 250, 254, 0.9); font-size: 1.2rem; margin-bottom: 1.5rem; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">
                 Accede al <strong>Panel de Control</strong> y empezar a proteger tu red IoT
            </p>
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚀</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(240, 250, 254, 0.4);">
        <p style="margin: 0;">🛡️ Sistema de Detección de Anomalías IoT</p>
        <p style="margin: 0.5rem 0 0 0;">© 2026 Innovasic | UCC</p>
    </div>
    """, unsafe_allow_html=True)

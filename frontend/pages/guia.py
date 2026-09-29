"""
Página de Guía Educativa Completa del Sistema IDS para IoT.
Explicación detallada y accesible de todos los conceptos, modelos y funcionalidades.
"""

import streamlit as st
from config.theme import get_current_theme
from config.i18n import get_language, t, t_list
from pathlib import Path
import base64


def show_guia_page():
    """Página educativa completa sobre el sistema IDS."""

    theme = get_current_theme()
    c = theme.colors

    st.markdown("""
    <style>
        .guide-translated { display: none; }
        .guide-model-card.en > *:not(.guide-translated),
        .guide-attack-card.en > *:not(.guide-translated) { display: none; }
        .guide-model-card.en > .guide-translated,
        .guide-attack-card.en > .guide-translated { display: block; }
    </style>
    """, unsafe_allow_html=True)
    
    # helper base64
    # el directorio "img" vive en la raíz del repo, no dentro de frontend/pages.
    img_dir = Path(__file__).parent.parent.parent / "img"
    def _b64(fname):
        p = img_dir / fname
        if not p.exists():
            return None
        ext = p.suffix.lstrip('.')
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{ext};base64,{data}"

    # Background image encoded
    img3_b64 = _b64("img3.png") or ""
    
    # Hero Section con imagen de fondo
    st.markdown(f"""
    <style>
        .guia-header {{
            position: relative;
            background: url('{img3_b64}') center center / cover no-repeat;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .guia-header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: {c.hero_overlay};
            border-radius: 20px;
            z-index: 1;
        }}
        .guia-header-content {{
            position: relative;
            z-index: 2;
            text-align: center;
        }}
    </style>
    <div class="guia-header">
        <div class="guia-header-content">
            <h1 style="color: {c.hero_title}; font-size: 3rem; margin-bottom: 1rem; 
                       text-shadow: 2px 2px 8px rgba(0,0,0,0.4);">
                {t('guide_title')}
            </h1>
            <h3 style="color: {c.hero_subtitle}; font-weight: 300; margin-bottom: 0; font-size: 1.3rem;">
                {t('guide_subtitle')}
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==================== ¿QUÉ ES ESTE SISTEMA? ====================
    
    st.markdown(f"## {t('what_is_ids')}")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {c.success_light} 0%, rgba(16, 185, 129, 0.05) 100%); 
                padding: 2rem; border-radius: 15px; border-left: 5px solid {c.success}; margin: 1.5rem 0;">
        
    <h3 style="color: {c.success}; margin-top: 0;">{t('guide_simple_explanation')}</h3>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify; margin-bottom: 1.5rem;">
        {t('guide_intro_paragraph_1')}
    </p>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify; margin-bottom: 1.5rem;">
        {t('guide_intro_paragraph_2')}
    </p>
    
    <h3 style="color: {c.success}; margin-top: 2rem;">{t('guide_why_important')}</h3>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify;">
        {t('guide_iot_risk')}
    </p>
    
    <ul style="font-size: 1.1rem; line-height: 1.8; margin-left: 1.5rem;">
        {''.join(f'<li>{item}</li>' for item in t_list('guide_iot_risk_items'))}
    </ul>
    
    </div>
    """, unsafe_allow_html=True)

    # ==================== CÓMO FUNCIONA NUESTRO SISTEMA ====================
    
    st.markdown("---")
    st.markdown(f"## {t('how_system_works')}")
    
    # Tabs para cada etapa del proceso
    tab1, tab2, tab3, tab4 = st.tabs([t('capture_tab'), t('analysis_tab'), t('detection_tab'), t('alert_tab')])
    
    with tab1:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: rgba(19, 131, 167, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: {c.heading_secondary};">{t('guide_capture_title')}</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            {t('guide_capture_text')}
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            
        </p>
        
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            {''.join(f'<li>{item}</li>' for item in t_list('guide_capture_items'))}
        </ul>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            {t('guide_capture_analogy')}
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: {c.warning_light}; border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: {c.warning};">{t('guide_analysis_title')}</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            {t('guide_analysis_text')}
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            
        </p>
        
        <ol style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            {''.join(f'<li>{item}</li>' for item in t_list('guide_analysis_items'))}
        </ol>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            {t('guide_analysis_analogy')}
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: {c.surface_variant}; border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: {c.heading_secondary};">{t('guide_detection_title')}</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            {t('guide_detection_text')}
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            
        </p>
        
        <ol style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            {''.join(f'<li>{item}</li>' for item in t_list('guide_detection_items'))}
        </ol>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            {t('guide_detection_analogy')}
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: rgba(239, 68, 68, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: {c.error};">{t('guide_alert_title')}</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            {t('guide_alert_text')}
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            
        </p>
        
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            {''.join(f'<li>{item}</li>' for item in t_list('guide_alert_items'))}
        </ul>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            {t('guide_alert_analogy')}
        </p>
        
        </div>
        """, unsafe_allow_html=True)

    # ==================== MODELOS DE IA EXPLICADOS ====================
    
    st.markdown("---")
    st.markdown(f"## {t('explained_ai_models')}")
    
    st.info(t("guide_models_note"))

    st.info(t("guide_models_added"))
    
    # IForest
    with st.expander(t("iforest_guide_title"), expanded=False):
        st.markdown(f"""
        <div class="guide-model-card {get_language()}" style="padding: 1rem; background: {c.success_light}; border-radius: 10px;">
        <div class="guide-translated">{t('guide_iforest_body')}</div>
        
            <h4 style="color: {c.success};">{t('model_what_how')}</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>Isolation Forest</strong> funciona con un principio simple pero poderoso: 
            <strong>las anomalías son raras y diferentes</strong>, por lo que son más fáciles de "aislar" 
            del resto de los datos.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía del mundo real:</strong><br>
            Imagina una fiesta donde casi todos visten de manera formal. Si llega alguien con disfraz 
            de dinosaurio, es muy fácil "aislarlo" visualmente del resto. No necesitas revisar a cada 
            persona de la fiesta para notar que el dinosaurio es diferente.
        </p>
        
            <h4 style="color: {c.success}; margin-top: 1.5rem;">{t('model_technical')}</h4>
        
        <ol style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>Construcción de árboles</strong>: Crea múltiples "árboles de decisión" aleatorios</li>
            <li><strong>Partición recursiva</strong>: Divide los datos repetidamente con criterios aleatorios</li>
            <li><strong>Medición de profundidad</strong>: Cuenta cuántos pasos necesita para aislar cada punto
                <ul style="margin-top: 0.5rem;">
                    <li>✅ Datos <strong>normales</strong>: requieren muchos pasos (están "mezclados" con otros)</li>
                    <li>🚨 <strong>Anomalías</strong>: se aíslan rápidamente (están "solas")</li>
                </ul>
            </li>
            <li><strong>Puntuación de anomalía</strong>: Calcula un score promedio de todos los árboles</li>
        </ol>
        
        <h4 style="color: {c.success}; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>⚡ <strong>Muy rápido</strong>: Excelente para grandes volúmenes de datos</li>
            <li>💪 <strong>Eficiente con alta dimensionalidad</strong>: Funciona bien con muchas características</li>
            <li>🎯 <strong>No requiere etiquetas</strong>: Aprende solo del tráfico normal</li>
            <li>🔄 <strong>Bajo uso de memoria</strong>: Ideal para dispositivos con recursos limitados</li>
        </ul>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>No clasifica <strong>tipos específicos</strong> de ataques (solo detecta "normal" vs "anómalo")</li>
            <li>Puede tener <strong>falsos positivos</strong> si el tráfico normal tiene mucha variación</li>
        </ul>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Ideal para <strong>detección general de anomalías</strong> cuando tienes grandes volúmenes de tráfico 
            y necesitas respuestas rápidas. Perfecto como primera línea de defensa.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # OCSVM
    with st.expander(t("ocsvm_guide_title"), expanded=False):
        st.markdown(f"""
        <div class="guide-model-card {get_language()}" style="padding: 1rem; background: rgba(33, 150, 243, 0.08); border-radius: 10px;">
        <div class="guide-translated">{t('guide_ocsvm_body')}</div>
        
            <h4 style="color: {c.heading_secondary};">{t('model_what_how')}</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>One-Class SVM</strong> aprende a crear una "frontera" o "perímetro de seguridad" 
            alrededor del tráfico normal. Cualquier cosa que caiga fuera de este perímetro se considera anómala.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía del mundo real:</strong><br>
            Imagina que dibujas un círculo de tiza alrededor de todos tus vecinos en una foto aérea 
            del barrio. Cualquier persona que aparezca fuera de ese círculo sería considerada un "visitante" 
            o potencial intruso.
        </p>
        
            <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">{t('model_technical')}</h4>
        
        <ol style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>Aprendizaje de la normalidad</strong>: Estudia solo ejemplos de tráfico legítimo</li>
            <li><strong>Construcción del hiperplano</strong>: Crea una "superficie" matemática que envuelve 
                los datos normales en un espacio multidimensional</li>
            <li><strong>Transformación kernel</strong>: Utiliza trucos matemáticos (kernels) para manejar 
                patrones complejos y no lineales</li>
            <li><strong>Cálculo de distancia</strong>: Para cada nuevo dato, calcula qué tan lejos está 
                de la "zona de seguridad"
                <ul style="margin-top: 0.5rem;">
                    <li>✅ <strong>Dentro del perímetro</strong>: Tráfico normal</li>
                    <li>🚨 <strong>Fuera del perímetro</strong>: Posible amenaza</li>
                </ul>
            </li>
        </ol>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎯 <strong>Alta precisión</strong>: Excelente para definir límites claros de normalidad</li>
            <li>🔧 <strong>Flexible con kernels</strong>: Puede adaptarse a patrones complejos</li>
            <li>💪 <strong>Robusto</strong>: Funciona bien incluso con outliers en los datos de entrenamiento</li>
            <li>📊 <strong>Puntuación de confianza</strong>: Proporciona un score que indica "qué tan anómalo" es algo</li>
        </ul>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🐌 <strong>Más lento</strong> que IForest en conjuntos de datos grandes</li>
            <li>⚙️ <strong>Requiere ajuste de parámetros</strong>: Necesita configuración cuidadosa</li>
            <li>💾 <strong>Uso de memoria</strong>: Puede requerir más recursos computacionales</li>
        </ul>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Perfecto cuando necesitas <strong>alta precisión</strong> y tienes un buen conjunto de datos 
            de tráfico normal. Ideal para redes con patrones de tráfico bien definidos y estables.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # K-MEANS
    with st.expander(t("kmeans_guide_title"), expanded=False):
        st.markdown(f"""
        <div class="guide-model-card {get_language()}" style="padding: 1rem; background: {c.warning_light}; border-radius: 10px;">
        <div class="guide-translated">{t('guide_kmeans_body')}</div>
        
            <h4 style="color: {c.warning};">{t('model_what_how')}</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>K-MEANS</strong> es un algoritmo de agrupamiento (clustering) que organiza el tráfico 
            en diferentes "grupos" o "clusters" según sus similitudes. Luego identifica qué grupos representan 
            tráfico normal y cuáles son sospechosos.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía del mundo real:</strong><br>
            Imagina que tienes una caja llena de frutas mixtas. K-MEANS sería como separar automáticamente 
            las manzanas, naranjas, plátanos y uvas en grupos distintos basándose en color, forma y tamaño. 
            Si aparece algo extraño (como una piedra), quedará en un grupo aparte o muy lejos de los demás.
        </p>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">{t('model_technical')}</h4>
        
        <ol style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>Inicialización de centroides</strong>: Elige K puntos centrales aleatorios 
                (representantes de cada grupo)</li>
            <li><strong>Asignación de puntos</strong>: Asigna cada paquete de datos al centroide más cercano</li>
            <li><strong>Recalculación</strong>: Actualiza la posición de los centroides basándose en 
                el promedio de todos los puntos asignados</li>
            <li><strong>Iteración</strong>: Repite los pasos 2 y 3 hasta que los grupos se estabilicen</li>
            <li><strong>Identificación de anomalías</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>✅ <strong>Clusters grandes</strong>: Probablemente tráfico normal</li>
                    <li>⚠️ <strong>Puntos alejados</strong>: Posibles anomalías</li>
                    <li>🚨 <strong>Clusters pequeños específicos</strong>: Pueden indicar ataques conocidos</li>
                </ul>
            </li>
        </ol>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify; margin-top: 1rem;">
            <strong>🎯 Clasificación multiclase:</strong><br>
            En nuestro sistema, K-MEANS ha sido entrenado para reconocer clusters específicos de diferentes 
            tipos de ataques, permitiendo clasificación detallada:
        </p>
        
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            <li>✅ <strong>Normal</strong>: Tráfico legítimo</li>
            <li>🔴 <strong>DDoS_TCP</strong>: Ataque de denegación de servicio vía TCP</li>
            <li>🟠 <strong>DDoS_UDP</strong>: Ataque de denegación de servicio vía UDP</li>
            <li>🔵 <strong>Reconnaissance</strong>: Escaneo y reconocimiento de red</li>
        </ul>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎯 <strong>Clasificación detallada</strong>: Identifica tipos específicos de ataques</li>
            <li>⚡ <strong>Simple y rápido</strong>: Fácil de entender e implementar</li>
            <li>📊 <strong>Interpretable</strong>: Los clusters se pueden analizar y comprender</li>
            <li>🔄 <strong>Adaptable</strong>: Puede descubrir nuevos patrones automáticamente</li>
        </ul>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎲 <strong>Sensible a inicialización</strong>: Resultados pueden variar entre ejecuciones</li>
            <li>🔢 <strong>Requiere definir K</strong>: Debes especificar cuántos grupos buscar</li>
            <li>⭕ <strong>Asume clusters esféricos</strong>: Puede tener problemas con formas irregulares</li>
        </ul>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Ideal cuando necesitas <strong>clasificar tipos específicos de amenazas</strong> y entender 
            exactamente qué tipo de ataque está ocurriendo. Excelente para análisis forense y generación 
            de reportes detallados.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # AUTOENCODER
    with st.expander(t("autoencoder_guide_title"), expanded=False):
        st.markdown(f"""
        <div class="guide-model-card {get_language()}" style="padding: 1rem; background: {c.surface_variant}; border-radius: 10px;">
        <div class="guide-translated">{t('guide_autoencoder_body')}</div>
        
        <h4 style="color: {c.heading_secondary};">{t('model_what_how')}</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            Un <strong>Autoencoder</strong> es una red neuronal profunda (Deep Learning) que aprende a 
            "comprimir" y "reconstruir" datos. Piensa en ello como aprender la "esencia" del tráfico normal 
            para poder reconocer cuando algo no encaja.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía del mundo real:</strong><br>
            Imagina que eres un experto en arte que ha estudiado miles de obras de Picasso. Has aprendido 
            su "esencia" tan bien que puedes:
            <ul style="margin-top: 0.5rem;">
                <li>Recrear un cuadro de Picasso desde un simple boceto</li>
                <li>Detectar inmediatamente si una obra NO es de Picasso</li>
                <li>Identificar qué período o estilo específico de Picasso representa</li>
            </ul>
        </p>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">{t('model_technical')}</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            El Autoencoder tiene dos partes principales:
        </p>
        
        <ol style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>Encoder (Codificador)</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>Comprime los datos de entrada en una representación más pequeña</li>
                    <li>Extrae las características más importantes</li>
                    <li>Es como hacer un "resumen" inteligente de cada paquete</li>
                </ul>
            </li>
            <li><strong>Decoder (Decodificador)</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>Intenta reconstruir los datos originales desde el resumen</li>
                    <li>Si conoce bien el patrón, la reconstrucción será casi perfecta</li>
                    <li>Si el patrón es extraño (anomalía), habrá mucho error de reconstrucción</li>
                </ul>
            </li>
            <li><strong>Clasificador Multiclase</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>Añadido al final para clasificar el tipo específico de tráfico</li>
                    <li>Entrenado con ejemplos etiquetados de cada tipo de ataque</li>
                    <li>Proporciona probabilidades para cada clase</li>
                </ul>
            </li>
        </ol>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">🎯 Proceso de detección:</h4>
        
        <ol style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>Análisis de error de reconstrucción</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>Error bajo → Tráfico conocido (normal o ataque conocido)</li>
                    <li>Error alto → Anomalía nunca vista antes</li>
                </ul>
            </li>
            <li><strong>Clasificación específica</strong>:
                <ul style="margin-top: 0.5rem;">
                    <li>✅ <strong>Normal</strong> (probabilidad ≥ umbral)</li>
                    <li>🔴 <strong>DDoS_TCP</strong></li>
                    <li>🟠 <strong>DDoS_UDP</strong></li>
                    <li>🔵 <strong>Reconnaissance</strong></li>
                </ul>
            </li>
        </ol>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🧠 <strong>Aprendizaje profundo</strong>: Captura patrones muy complejos y sutiles</li>
            <li>🎯 <strong>Clasificación multiclase precisa</strong>: Identifica tipos específicos de ataques</li>
            <li>🔍 <strong>Doble detección</strong>: Error de reconstrucción + clasificación</li>
            <li>🆕 <strong>Detecta ataques nuevos</strong>: Puede identificar amenazas nunca vistas</li>
            <li>📊 <strong>Probabilidades</strong>: Proporciona confianza en las predicciones</li>
            <li>💪 <strong>Robusto</strong>: Funciona bien con datos ruidosos o incompletos</li>
        </ul>
        
        <h4 style="color: {c.warning}; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🐌 <strong>Más lento</strong>: Requiere más procesamiento que otros modelos</li>
            <li>💾 <strong>Uso de recursos</strong>: Necesita más memoria y CPU</li>
            <li>⚙️ <strong>Complejo de entrenar</strong>: Requiere ajuste cuidadoso de hiperparámetros</li>
            <li>📚 <strong>Necesita muchos datos</strong>: Funciona mejor con grandes conjuntos de entrenamiento</li>
        </ul>
        
        <h4 style="color: {c.heading_secondary}; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            El modelo más <strong>potente y preciso</strong> del sistema. Ideal cuando necesitas la máxima 
            precisión, clasificación detallada de amenazas, y tienes recursos computacionales suficientes. 
            Perfecto para análisis críticos de seguridad.
        </p>
        
        </div>
        """, unsafe_allow_html=True)

    # ==================== TIPOS DE ATAQUES EXPLICADOS ====================
    
    st.markdown("---")
    st.markdown(f"## {t('detected_attack_types')}")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div class="guide-attack-card {get_language()}" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid {c.error}; margin: 1rem 0; height: 100%;">
        <div class="guide-translated">{t('guide_ddos_tcp_body')}</div>
        
        <h3 style="color: {c.error};">🔴 DDoS TCP</h3>
        <h4 style="color: {c.error}; font-size: 1.1rem;">Ataque de Denegación de Servicio vía TCP</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>¿Qué es?</strong><br>
            Un ataque donde el atacante inunda tu red con miles o millones de solicitudes TCP falsas, 
            sobrecargando tus dispositivos hasta que no puedan responder a usuarios legítimos.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía:</strong><br>
            Es como si alguien hiciera miles de llamadas telefónicas falsas a un restaurante 
            simultáneamente, bloqueando las líneas para que clientes reales no puedan hacer reservas.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8;">
            <strong>🔍 Cómo lo detectamos:</strong>
        </p>
        <ul style="font-size: 1rem; line-height: 1.7;">
            <li>Picos anormales en tráfico TCP</li>
            <li>Muchas conexiones incompletas (SYN flood)</li>
            <li>Solicitudes desde múltiples IPs en poco tiempo</li>
            <li>Patrones de timing artificiales</li>
        </ul>
        
        <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>🛡️ Acciones recomendadas:</strong>
        </p>
        <ul style="font-size: 1rem; line-height: 1.7;">
            <li>✅ Activar <strong>SYN cookies</strong> en el firewall</li>
            <li>✅ Configurar <strong>límites de tasa de conexión</strong></li>
            <li>✅ Usar <strong>ACL para bloquear IPs</strong> sospechosas</li>
            <li>✅ Implementar <strong>filtrado de paquetes</strong> malformados</li>
        </ul>
        
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="guide-attack-card {get_language()}" style="background: linear-gradient(135deg, {c.warning_light} 0%, rgba(245, 158, 11, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid {c.warning}; margin: 1rem 0; height: 100%;">
        <div class="guide-translated">{t('guide_ddos_udp_body')}</div>
        
        <h3 style="color: {c.warning};">🟠 DDoS UDP</h3>
        <h4 style="color: {c.warning}; font-size: 1.1rem;">Ataque de Denegación de Servicio vía UDP</h4>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>¿Qué es?</strong><br>
            Similar al DDoS TCP, pero utiliza el protocolo UDP que no requiere confirmación. 
            El atacante puede enviar grandes cantidades de paquetes UDP a puertos aleatorios, 
            consumiendo ancho de banda y recursos.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
            <strong>💡 Analogía:</strong><br>
            Es como enviar miles de cartas a direcciones aleatorias de un edificio. El portero 
            (tu dispositivo) debe verificar cada carta, consumiendo todo su tiempo y energía.
        </p>
        
        <p style="font-size: 1.05rem; line-height: 1.8;">
            <strong>🔍 Cómo lo detectamos:</strong>
        </p>
        <ul style="font-size: 1rem; line-height: 1.7;">
            <li>Tráfico UDP excesivo a puertos aleatorios</li>
            <li>Muchos mensajes ICMP "puerto no alcanzable"</li>
            <li>Amplificación de DNS/NTP</li>
            <li>Paquetes de tamaño uniforme sospechoso</li>
        </ul>
        
        <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>🛡️ Acciones recomendadas:</strong>
        </p>
        <ul style="font-size: 1rem; line-height: 1.7;">
            <li>✅ <strong>Permitir solo puertos UDP necesarios</strong></li>
            <li>✅ Aplicar <strong>límites de tasa UDP</strong></li>
            <li>✅ Usar <strong>null routing</strong> para IPs atacantes</li>
            <li>✅ Configurar <strong>validación de origen</strong> (uRPF)</li>
        </ul>
        
        </div>
        """, unsafe_allow_html=True)
    
    # Reconnaissance
    st.markdown(f"""
    <div class="guide-attack-card {get_language()}" style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.05) 100%); 
                padding: 1.5rem; border-radius: 15px; border-left: 5px solid {c.primary}; margin: 1rem 0;">
    <div class="guide-translated">{t('guide_recon_body')}</div>
    
    <h3 style="color: {c.heading_secondary};">🔵 Reconnaissance (Reconocimiento)</h3>
    <h4 style="color: {c.heading_secondary}; font-size: 1.1rem;">{t('reconnaissance_subtitle')}</h4>
    
    <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
        <strong>¿Qué es?</strong><br>
        Es la fase de "reconocimiento" donde los atacantes escanean tu red para identificar:
        <ul style="margin-top: 0.5rem;">
            <li>Qué dispositivos están activos</li>
            <li>Qué servicios están ejecutando</li>
            <li>Qué puertos están abiertos</li>
            <li>Qué vulnerabilidades pueden explotar</li>
        </ul>
    </p>
    
    <p style="font-size: 1.05rem; line-height: 1.8; text-align: justify;">
        <strong>💡 Analogía:</strong><br>
        Es como un ladrón caminando por tu vecindario tomando notas: "Esta casa tiene alarma, 
        aquella puerta trasera está mal cerrada, este perro parece agresivo". Están recopilando 
        información para un ataque futuro.
    </p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem;">
        <div>
            <p style="font-size: 1.05rem; line-height: 1.8;">
                <strong>🔍 Cómo lo detectamos:</strong>
            </p>
            <ul style="font-size: 1rem; line-height: 1.7;">
                <li>Escaneo de puertos (Port Scanning)</li>
                <li>Ping sweeps (múltiples ICMP)</li>
                <li>Escaneo de vulnerabilidades</li>
                <li>Intentos de fingerprinting del SO</li>
                <li>Patrones de nmap, masscan, etc.</li>
            </ul>
        </div>
        <div>
            <p style="font-size: 1.05rem; line-height: 1.8;">
                <strong>🛡️ Acciones recomendadas:</strong>
            </p>
            <ul style="font-size: 1rem; line-height: 1.7;">
                <li>✅ <strong>Restringir respuestas ICMP</strong></li>
                <li>✅ <strong>Exponer solo puertos necesarios</strong></li>
                <li>✅ Configurar <strong>límites anti-scan</strong></li>
                <li>✅ Usar <strong>honeypots</strong> para detectar escaneos</li>
                <li>✅ <strong>Bloquear IPs</strong> que hacen escaneos</li>
            </ul>
        </div>
    </div>
    
    <div style="background: rgba(255, 235, 59, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1.5rem; border: 1px solid rgba(255, 235, 59, 0.3);">
        <p style="font-size: 1rem; line-height: 1.7; margin: 0;">
            <strong>⚠️ Importante:</strong> El reconnaissance suele ser la primera fase de un ataque más grande. 
            Detectarlo temprano te da tiempo para reforzar tus defensas antes de que ocurra el ataque real.
        </p>
    </div>
    
    </div>
    """, unsafe_allow_html=True)

    # ==================== INTERPRETACIÓN DE MÉTRICAS ====================
    
    st.markdown("---")
    st.markdown(f"## {t('understanding_metrics')}")
    
    st.markdown(f"""
    <div style="background: rgba(103, 58, 183, 0.1); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0;">
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            {t('guide_metrics_intro_html')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para métricas
    tab_int, tab_ext, tab_rend = st.tabs([t("internal_tab"), t("external_tab"), t("performance_tab")])
    
    with tab_int:
        st.markdown(t("internal_metrics_heading"))
        
        st.write(t("metrics_intro"))
        
        # Silhouette Score
        st.success(t("silhouette_title"))
        
        st.write(t("what_measures"))
        st.write(t("silhouette_detail"))
        
        st.write(t("analogy"))
        st.write(t("silhouette_analogy_detail"))
        
        st.write(t("how_to_interpret"))
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write(t("silhouette_perfect"))
            st.write(t("silhouette_excellent"))
            st.write(t("silhouette_good"))
        with col2:
            st.write(t("silhouette_fair"))
            st.write(t("silhouette_poor"))
            st.write(t("silhouette_bad"))
        
        st.divider()
        
        # Calinski-Harabasz
        st.info(t("calinski_index"))
        
        st.write(t("what_measures_heading"))
        st.write(t("calinski_detail"))
        
        st.write(t("analogy_heading"))
        st.write(t("calinski_analogy"))
        
        st.write(t("interpret_heading"))
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write(t("calinski_excellent"))
            st.write(t("calinski_good"))
        with col2:
            st.write(t("calinski_fair"))
            st.write(t("calinski_poor"))
        
        st.warning(t("calinski_note"))
        
        st.divider()
        
        # Davies-Bouldin
        st.warning(t("davies_index"))
        
        st.write(t("what_measures_heading"))
        st.write(t("davies_detail"))
        
        st.write(t("analogy_heading"))
        st.write(t("davies_analogy"))
        
        st.write(t("interpret_heading"))
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write(t("davies_perfect"))
            st.write(t("davies_excellent"))
            st.write(t("davies_good"))
        with col2:
            st.write(t("davies_fair"))
            st.write(t("davies_poor"))
        
        st.error(t("davies_note"))
        
        st.divider()
        
        # Combinación de métricas
        st.subheader(t("combine_metrics"))
        
        st.write(t("complete_evaluation"))
        
        st.success(t("excellent_metrics"))
        
        st.warning(t("acceptable_metrics"))
        
        st.error(t("poor_metrics"))

    with tab_ext:
        st.markdown(t("external_metrics_heading"))

        st.write(t("external_metrics_intro"))

        st.info(t("external_metrics_when"))

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.success(t("accuracy_metric"))
            st.write(t("accuracy_detail"))
            st.write(t("accuracy_ideal"))

            st.success(t("precision_metric"))
            st.write(t("precision_detail"))
            st.write(t("precision_ideal"))

            st.success(t("recall_metric"))
            st.write(t("recall_detail"))
            st.write(t("recall_ideal"))

        with col2:
            st.success(t("f1_metric"))
            st.write(t("f1_detail"))
            st.write(t("f1_ideal"))

            st.success(t("roc_metric"))
            st.write(t("roc_detail"))
            st.write(t("roc_ideal"))

            st.success(t("confusion_metric"))
            st.write(t("confusion_detail"))
            st.write(t("confusion_ideal"))

        st.divider()

        st.markdown(t("practical_interpretation"))
        st.write(t("practical_metrics"))
    
    with tab_rend:
        st.markdown(t("performance_heading"))
        
        st.write(t("performance_intro"))
        
        # Grid de métricas de rendimiento (2 columnas)
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.info(t("cpu_metric"))
            st.write(t("what_measures_short"))
            st.write(t("cpu_detail"))
            
            st.write(t("analogy_short"))
            st.write(t("cpu_analogy"))
            
            st.write(t("typical_values"))
            st.write(t("cpu_low")); st.write(t("cpu_moderate")); st.write(t("cpu_high")); st.write(t("cpu_overload"))
        
        with col2:
            st.info(t("ram_metric"))
            st.write(t("what_measures_short"))
            st.write(t("ram_detail"))
            
            st.write(t("analogy_short"))
            st.write(t("ram_analogy"))
            
            st.write(t("typical_values")); st.write(t("ram_healthy")); st.write(t("ram_moderate")); st.write(t("ram_high")); st.write(t("ram_full"))
        
        st.divider()
        
        col3, col4 = st.columns(2, gap="medium")
        
        with col3:
            st.warning(t("disk_metric"))
            st.write(t("what_measures_short"))
            st.write(t("disk_detail"))
            
            st.write(t("analogy_short"))
            st.write(t("disk_analogy"))
            
            st.write(t("typical_values")); st.write(t("disk_enough")); st.write(t("disk_clean")); st.write(t("disk_low")); st.write(t("disk_critical"))
        
        with col4:
            st.success(t("time_metric"))
            st.write(t("what_measures_short"))
            st.write(t("time_detail"))
            
            st.write(t("importance_short"))
            st.write(t("time_importance"))
            
            st.write(t("typical_packets")); st.write(t("time_very_fast")); st.write(t("time_fast")); st.write(t("time_fair")); st.write(t("time_slow"))
        
        st.divider()
        
        # Tabla comparativa
        st.subheader(t("models_comparison"))
        
        # Crear tabla con pandas
        import pandas as pd
        
        comparacion = pd.DataFrame({
            t("guide_table_model"): ["IForest", "OCSVM", "K-MEANS", "Autoencoder", "DecisionTree", "ExtraTrees", "LogisticRegression", "RandomForest"],
            t("guide_table_speed"): t_list("guide_table_speed_values"),
            t("guide_table_cpu"): t_list("guide_table_cpu_values"),
            t("guide_table_ram"): t_list("guide_table_ram_values")
        })
        
        st.dataframe(comparacion, use_container_width=True, hide_index=True)

    # ==================== GUÍA DE USO PASO A PASO ====================
    
    st.markdown("---")
    st.markdown(f"## {t('step_by_step_guide')}")
    
    steps = [
        {
            "icon": "🔌",
            "title_key": "steps_model_title", "description_key": "steps_model_desc", "details_key": "steps_model_details", "tip_key": "steps_model_tip"
        },
        {
            "icon": "📊",
            "title_key": "steps_metric_title", "description_key": "steps_metric_desc", "details_key": "steps_metric_details", "tip_key": "steps_metric_tip"
        },
        {
            "icon": "📡",
            "title_key": "steps_capture_title", "description_key": "steps_capture_desc", "details_key": "steps_capture_details", "tip_key": "steps_capture_tip"
        },
        {
            "icon": "🖱️",
            "title_key": "steps_predict_title", "description_key": "steps_predict_desc", "details_key": "steps_predict_details", "tip_key": "steps_predict_tip"
        },
        {
            "icon": "📊",
            "title_key": "steps_results_title", "description_key": "steps_results_desc", "details_key": "steps_results_details", "tip_key": "steps_results_tip"
        },
        {
            "icon": "📄",
            "title_key": "steps_report_title", "description_key": "steps_report_desc", "details_key": "steps_report_details", "tip_key": "steps_report_tip"
        }
    ]
    
    for idx, step in enumerate(steps, 1):
        color_map = {
            1: c.success,
            2: c.primary,
            3: c.warning,
            4: c.tertiary,
            5: c.error,
            6: c.primary
        }
        color = color_map.get(idx, c.quaternary)
        
        details_html = ''.join([f'<li>{detail}</li>' for detail in t(step['details_key'])])
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid {color}; margin: 1rem 0;">
            <h3 style="color: {color}; margin-top: 0;">
                <span style="font-size: 2rem; margin-right: 0.5rem;">{step['icon']}</span>
                {t(step['title_key'])}
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
                {t(step['description_key'])}
            </p>
            <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
                {details_html}
            </ul>
            </ul>
            <div style="background: rgba(255, 235, 59, 0.15); padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 3px solid {c.warning};">
                <strong style="color: {c.warning};">{t('guide_tip')}</strong> {t(step['tip_key'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==================== PREGUNTAS FRECUENTES ====================
    
    st.markdown("---")
    st.markdown(f"## {t('faq')}")
    
    with st.expander(t("faq_accuracy_title"), expanded=False):
        st.markdown(t("faq_accuracy"))
    
    with st.expander(t("faq_packets_title"), expanded=False):
        st.markdown(t("faq_packets"))
    
    with st.expander(t("faq_attack_title"), expanded=False):
        st.markdown(t("faq_attack"))
    
    with st.expander(t("faq_multiple_title"), expanded=False):
        st.markdown(t("faq_multiple"))
    
    with st.expander(t("faq_zero_day_title"), expanded=False):
        st.markdown(t("faq_zero_day"))
    
    with st.expander(t("faq_impact_title"), expanded=False):
        st.markdown(t("faq_impact"))

    # ==================== CONSEJOS Y MEJORES PRÁCTICAS ====================
    
    st.markdown("---")
    st.markdown(f"## {t('best_practices')}")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {c.success_light} 0%, rgba(16, 185, 129, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 100%;">
            <h3 style="color: {c.success};">{t('guide_good_practices_title')}</h3>
            <ul style="font-size: 1.05rem; line-height: 1.8;">
                {''.join(f'<li>{item}</li>' for item in t_list('guide_good_practices'))}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 100%;">
            <h3 style="color: {c.error};">{t('guide_common_errors_title')}</h3>
            <ul style="font-size: 1.05rem; line-height: 1.8;">
                {''.join(f'<li>{item}</li>' for item in t_list('guide_common_errors'))}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==================== FOOTER DE LA GUÍA ====================
    img1_url = "app/static/img1.jpg"
    
    st.markdown("---")
    st.markdown(f"""
    <style>
        .guia-footer {{
            position: relative;
            text-align: center;
            padding: 3rem 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            overflow: hidden;
            background: url('{img1_url}') center center / cover no-repeat;
        }}
        .guia-footer::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: {c.hero_overlay};
            border-radius: 15px;
            z-index: 1;
        }}
        .guia-footer-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="guia-footer">
        <div class="guia-footer-content">
            <h2 style="color: {c.hero_title}; margin-bottom: 1rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">{t('guide_congratulations')}</h2>
            <p style="color: {c.hero_subtitle}; font-size: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">
                {t('guide_footer_text')}
            </p>
            <p style="color: {c.hero_title}; font-size: 1.1rem; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">
                {t('guide_footer_cta')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

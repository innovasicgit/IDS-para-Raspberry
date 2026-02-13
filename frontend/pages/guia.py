"""
Página de Guía Educativa Completa del Sistema IDS para IoT.
Explicación detallada y accesible de todos los conceptos, modelos y funcionalidades.
"""

import streamlit as st


def show_guia_page():
    """Página educativa completa sobre el sistema IDS."""
    
    # URL de imagen estática (servida por Streamlit static serving)
    img3_url = "app/static/img3.png"
    
    # Hero Section con imagen de fondo
    st.markdown(f"""
    <style>
        .guia-header {{
            position: relative;
            background: url('{img3_url}') center center / cover no-repeat;
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
            background: rgba(0, 0, 0, 0.5);
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
            <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; 
                       text-shadow: 2px 2px 8px rgba(0,0,0,0.4);">
                📚 Guía Completa del Sistema IDS
            </h1>
            <h3 style="color: #F0FAFE; font-weight: 300; margin-bottom: 0; font-size: 1.3rem;">
                Todo lo que necesitas saber para proteger tu red IoT
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==================== ¿QUÉ ES ESTE SISTEMA? ====================
    
    st.markdown("## 🔰 ¿Qué es un Sistema de Detección de Intrusiones (IDS)?")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%); 
                padding: 2rem; border-radius: 15px; border-left: 5px solid #10B981; margin: 1.5rem 0;">
        
    <h3 style="color: #10B981; margin-top: 0;">💡 Explicación Simple</h3>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify; margin-bottom: 1.5rem;">
        Imagina que tu red de dispositivos conectados (IoT) es como tu casa. Un <strong>Sistema de Detección 
        de Intrusiones (IDS)</strong> actúa como un <strong>guardia de seguridad inteligente</strong> que observa 
        constantemente quién entra y sale, detectando cualquier comportamiento sospechoso.
    </p>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify; margin-bottom: 1.5rem;">
        En el mundo digital, los "visitantes" son <strong>paquetes de datos</strong> que viajan por tu red. 
        Nuestro sistema analiza cada uno de estos paquetes usando <strong>Inteligencia Artificial</strong> 
        para identificar si son "visitantes normales" (tráfico legítimo) o "intrusos" (amenazas de seguridad).
    </p>
    
    <h3 style="color: #10B981; margin-top: 2rem;">🎯 ¿Por qué es importante?</h3>
    
    <p style="font-size: 1.15rem; line-height: 1.9; text-align: justify;">
        Los dispositivos IoT (cámaras, sensores, termostatos inteligentes, etc.) son objetivos atractivos 
        para los atacantes porque muchas veces tienen <strong>seguridad limitada</strong>. Un ataque exitoso 
        puede permitir a los hackers:
    </p>
    
    <ul style="font-size: 1.1rem; line-height: 1.8; margin-left: 1.5rem;">
        <li>📹 <strong>Espiar</strong> tus cámaras de seguridad</li>
        <li>🔐 <strong>Robar</strong> información sensible</li>
        <li>💥 <strong>Usar tus dispositivos</strong> para atacar a otros (botnets)</li>
        <li>⚠️ <strong>Interrumpir</strong> servicios críticos</li>
    </ul>
    
    </div>
    """, unsafe_allow_html=True)

    # ==================== CÓMO FUNCIONA NUESTRO SISTEMA ====================
    
    st.markdown("---")
    st.markdown("## ⚙️ ¿Cómo Funciona Nuestro Sistema?")
    
    # Tabs para cada etapa del proceso
    tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Captura", "2️⃣ Análisis", "3️⃣ Detección", "4️⃣ Alerta"])
    
    with tab1:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(19, 131, 167, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: #1383A7;">📡 Captura de Tráfico de Red</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>¿Qué es?</strong><br>
            El sistema "escucha" toda la comunicación que pasa por tu red IoT, similar a como un micrófono 
            capta sonidos en una habitación.
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>¿Cómo lo hace?</strong><br>
            Utilizamos una herramienta llamada <code>tshark</code> que captura "paquetes de datos" 
            (pequeños fragmentos de información que viajan por la red). Cada paquete contiene:
        </p>
        
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            <li>🏠 <strong>Dirección de origen</strong>: ¿Quién envió el mensaje?</li>
            <li>🎯 <strong>Dirección de destino</strong>: ¿A quién va dirigido?</li>
            <li>📦 <strong>Tipo de protocolo</strong>: ¿Qué tipo de comunicación es? (TCP, UDP, ICMP)</li>
            <li>📏 <strong>Tamaño del paquete</strong>: ¿Cuántos datos se están enviando?</li>
            <li>⏱️ <strong>Marca de tiempo</strong>: ¿Cuándo se envió?</li>
            <li>🔢 <strong>Puertos</strong>: ¿Qué servicios están comunicándose?</li>
        </ul>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            <strong>💡 Analogía:</strong> Es como tener una cámara de seguridad que graba todo 
            lo que sucede en tu red, registrando cada "movimiento" (paquete de datos).
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(245, 158, 11, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: #F59E0B;">🔬 Análisis y Preprocesamiento</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>¿Qué sucede aquí?</strong><br>
            Los datos capturados se "limpian" y "organizan" para que la Inteligencia Artificial 
            pueda entenderlos mejor.
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>Pasos del procesamiento:</strong>
        </p>
        
        <ol style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            <li><strong>Normalización</strong>: Convertir todos los valores a un formato estándar 
                (como convertir todas las medidas a metros en vez de tener algunas en pies y otras en metros)</li>
            <li><strong>Filtrado</strong>: Eliminar datos irrelevantes o incompletos</li>
            <li><strong>Extracción de características</strong>: Identificar patrones importantes como:
                <ul style="margin-top: 0.5rem;">
                    <li>🔄 Frecuencia de paquetes por segundo</li>
                    <li>📊 Distribución de tamaños de paquetes</li>
                    <li>🌐 Patrones de comunicación entre dispositivos</li>
                    <li>⏰ Intervalos de tiempo entre paquetes</li>
                </ul>
            </li>
        </ol>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            <strong>💡 Analogía:</strong> Es como organizar y clasificar todas las grabaciones de la cámara 
            de seguridad, marcando eventos importantes como "persona entrando", "puerta abriéndose", etc.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(16, 78, 99, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: #104E63;">🧠 Detección con Inteligencia Artificial</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>¿Cómo detecta amenazas?</strong><br>
            Aquí es donde entra la magia de la Inteligencia Artificial. Los modelos han "aprendido" 
            cómo se ve el tráfico normal analizando miles o millones de ejemplos previos.
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>El proceso de detección:</strong>
        </p>
        
        <ol style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            <li><strong>Comparación con lo "normal"</strong>: El modelo compara los nuevos datos 
                con lo que ha aprendido que es tráfico legítimo</li>
            <li><strong>Cálculo de "extrañeza"</strong>: Asigna una puntuación que indica qué tan 
                diferente es el tráfico actual de lo esperado</li>
            <li><strong>Clasificación</strong>: Decide si el tráfico es:
                <ul style="margin-top: 0.5rem;">
                    <li>✅ <span style="color: #10B981;"><strong>Normal</strong></span>: 
                        Comportamiento esperado y seguro</li>
                    <li>⚠️ <span style="color: #F59E0B;"><strong>Sospechoso</strong></span>: 
                        Algo inusual pero no necesariamente peligroso</li>
                    <li>🚨 <span style="color: #EF4444;"><strong>Ataque</strong></span>: 
                        Amenaza identificada (DDoS, Reconnaissance, etc.)</li>
                </ul>
            </li>
        </ol>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            <strong>💡 Analogía:</strong> Es como un experto en seguridad que, después de años de experiencia, 
            puede identificar inmediatamente cuando algo no está bien solo observando el comportamiento 
            de las personas en un edificio.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(239, 68, 68, 0.1); border-radius: 12px; margin: 1rem 0;">
        
        <h3 style="color: #EF4444;">🚨 Generación de Alertas y Reportes</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>¿Qué pasa cuando se detecta una amenaza?</strong><br>
            El sistema genera alertas visuales y reportes detallados para que puedas tomar acción inmediata.
        </p>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>Tipos de alertas:</strong>
        </p>
        
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
            <li>📊 <strong>Gráficos en tiempo real</strong>: Visualización instantánea de amenazas detectadas</li>
            <li>📈 <strong>Métricas detalladas</strong>: Porcentajes de tráfico normal vs anómalo</li>
            <li>🎯 <strong>Clasificación de ataques</strong>: Identifica el tipo específico de amenaza</li>
            <li>📄 <strong>Reportes PDF</strong>: Documentos descargables con análisis completo</li>
            <li>💡 <strong>Recomendaciones</strong>: Sugerencias de acciones para mitigar el ataque</li>
        </ul>
        
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1.5rem;">
            <strong>💡 Analogía:</strong> Como cuando tu sistema de alarma de casa detecta un intruso 
            y te envía una notificación al móvil con imágenes, ubicación y recomendaciones de qué hacer.
        </p>
        
        </div>
        """, unsafe_allow_html=True)

    # ==================== MODELOS DE IA EXPLICADOS ====================
    
    st.markdown("---")
    st.markdown("## 🤖 Modelos de Inteligencia Artificial Explicados")
    
    st.info("""
    **💡 Nota importante**: Nuestro sistema utiliza 4 modelos diferentes de IA. 
    Cada uno tiene sus propias fortalezas y es mejor para detectar ciertos tipos de amenazas. 
    Puedes elegir el que mejor se adapte a tus necesidades o probar varios para comparar resultados.
    """)
    
    # IForest
    with st.expander("🌳 **IForest (Isolation Forest)** - El Detective de Patrones Extraños", expanded=False):
        st.markdown("""
        <div style="padding: 1rem; background: rgba(16, 185, 129, 0.08); border-radius: 10px;">
        
        <h4 style="color: #10B981;">🎯 ¿Qué es y cómo funciona?</h4>
        
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
        
        <h4 style="color: #10B981; margin-top: 1.5rem;">🔍 ¿Cómo lo hace técnicamente?</h4>
        
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
        
        <h4 style="color: #10B981; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>⚡ <strong>Muy rápido</strong>: Excelente para grandes volúmenes de datos</li>
            <li>💪 <strong>Eficiente con alta dimensionalidad</strong>: Funciona bien con muchas características</li>
            <li>🎯 <strong>No requiere etiquetas</strong>: Aprende solo del tráfico normal</li>
            <li>🔄 <strong>Bajo uso de memoria</strong>: Ideal para dispositivos con recursos limitados</li>
        </ul>
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>No clasifica <strong>tipos específicos</strong> de ataques (solo detecta "normal" vs "anómalo")</li>
            <li>Puede tener <strong>falsos positivos</strong> si el tráfico normal tiene mucha variación</li>
        </ul>
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Ideal para <strong>detección general de anomalías</strong> cuando tienes grandes volúmenes de tráfico 
            y necesitas respuestas rápidas. Perfecto como primera línea de defensa.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # OCSVM
    with st.expander("🎯 **OCSVM (One-Class SVM)** - El Guardián del Perímetro", expanded=False):
        st.markdown("""
        <div style="padding: 1rem; background: rgba(33, 150, 243, 0.08); border-radius: 10px;">
        
        <h4 style="color: #1383A7;">🎯 ¿Qué es y cómo funciona?</h4>
        
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
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">🔍 ¿Cómo lo hace técnicamente?</h4>
        
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
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎯 <strong>Alta precisión</strong>: Excelente para definir límites claros de normalidad</li>
            <li>🔧 <strong>Flexible con kernels</strong>: Puede adaptarse a patrones complejos</li>
            <li>💪 <strong>Robusto</strong>: Funciona bien incluso con outliers en los datos de entrenamiento</li>
            <li>📊 <strong>Puntuación de confianza</strong>: Proporciona un score que indica "qué tan anómalo" es algo</li>
        </ul>
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🐌 <strong>Más lento</strong> que IForest en conjuntos de datos grandes</li>
            <li>⚙️ <strong>Requiere ajuste de parámetros</strong>: Necesita configuración cuidadosa</li>
            <li>💾 <strong>Uso de memoria</strong>: Puede requerir más recursos computacionales</li>
        </ul>
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Perfecto cuando necesitas <strong>alta precisión</strong> y tienes un buen conjunto de datos 
            de tráfico normal. Ideal para redes con patrones de tráfico bien definidos y estables.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # K-MEANS
    with st.expander("🎨 **K-MEANS** - El Organizador Inteligente", expanded=False):
        st.markdown("""
        <div style="padding: 1rem; background: rgba(245, 158, 11, 0.08); border-radius: 10px;">
        
        <h4 style="color: #F59E0B;">🎯 ¿Qué es y cómo funciona?</h4>
        
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
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">🔍 ¿Cómo lo hace técnicamente?</h4>
        
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
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎯 <strong>Clasificación detallada</strong>: Identifica tipos específicos de ataques</li>
            <li>⚡ <strong>Simple y rápido</strong>: Fácil de entender e implementar</li>
            <li>📊 <strong>Interpretable</strong>: Los clusters se pueden analizar y comprender</li>
            <li>🔄 <strong>Adaptable</strong>: Puede descubrir nuevos patrones automáticamente</li>
        </ul>
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🎲 <strong>Sensible a inicialización</strong>: Resultados pueden variar entre ejecuciones</li>
            <li>🔢 <strong>Requiere definir K</strong>: Debes especificar cuántos grupos buscar</li>
            <li>⭕ <strong>Asume clusters esféricos</strong>: Puede tener problemas con formas irregulares</li>
        </ul>
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            Ideal cuando necesitas <strong>clasificar tipos específicos de amenazas</strong> y entender 
            exactamente qué tipo de ataque está ocurriendo. Excelente para análisis forense y generación 
            de reportes detallados.
        </p>
        
        </div>
        """, unsafe_allow_html=True)
    
    # AUTOENCODER
    with st.expander("🧬 **AUTOENCODER Multiclase** - El Experto en Patrones Profundos", expanded=False):
        st.markdown("""
        <div style="padding: 1rem; background: rgba(16, 78, 99, 0.08); border-radius: 10px;">
        
        <h4 style="color: #104E63;">🎯 ¿Qué es y cómo funciona?</h4>
        
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
        
        <h4 style="color: #104E63; margin-top: 1.5rem;">🔍 ¿Cómo lo hace técnicamente?</h4>
        
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
        
        <h4 style="color: #104E63; margin-top: 1.5rem;">🎯 Proceso de detección:</h4>
        
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
        
        <h4 style="color: #104E63; margin-top: 1.5rem;">✅ Ventajas</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🧠 <strong>Aprendizaje profundo</strong>: Captura patrones muy complejos y sutiles</li>
            <li>🎯 <strong>Clasificación multiclase precisa</strong>: Identifica tipos específicos de ataques</li>
            <li>🔍 <strong>Doble detección</strong>: Error de reconstrucción + clasificación</li>
            <li>🆕 <strong>Detecta ataques nuevos</strong>: Puede identificar amenazas nunca vistas</li>
            <li>📊 <strong>Probabilidades</strong>: Proporciona confianza en las predicciones</li>
            <li>💪 <strong>Robusto</strong>: Funciona bien con datos ruidosos o incompletos</li>
        </ul>
        
        <h4 style="color: #F59E0B; margin-top: 1.5rem;">⚠️ Limitaciones</h4>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>🐌 <strong>Más lento</strong>: Requiere más procesamiento que otros modelos</li>
            <li>💾 <strong>Uso de recursos</strong>: Necesita más memoria y CPU</li>
            <li>⚙️ <strong>Complejo de entrenar</strong>: Requiere ajuste cuidadoso de hiperparámetros</li>
            <li>📚 <strong>Necesita muchos datos</strong>: Funciona mejor con grandes conjuntos de entrenamiento</li>
        </ul>
        
        <h4 style="color: #1383A7; margin-top: 1.5rem;">🎯 Mejor uso</h4>
        <p style="font-size: 1.05rem; line-height: 1.8;">
            El modelo más <strong>potente y preciso</strong> del sistema. Ideal cuando necesitas la máxima 
            precisión, clasificación detallada de amenazas, y tienes recursos computacionales suficientes. 
            Perfecto para análisis críticos de seguridad.
        </p>
        
        </div>
        """, unsafe_allow_html=True)

    # ==================== TIPOS DE ATAQUES EXPLICADOS ====================
    
    st.markdown("---")
    st.markdown("## 🚨 Tipos de Ataques que Detectamos")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #EF4444; margin: 1rem 0; height: 100%;">
        
        <h3 style="color: #EF4444;">🔴 DDoS TCP</h3>
        <h4 style="color: #EF4444; font-size: 1.1rem;">Ataque de Denegación de Servicio vía TCP</h4>
        
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
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #F59E0B; margin: 1rem 0; height: 100%;">
        
        <h3 style="color: #F59E0B;">🟠 DDoS UDP</h3>
        <h4 style="color: #F59E0B; font-size: 1.1rem;">Ataque de Denegación de Servicio vía UDP</h4>
        
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
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.05) 100%); 
                padding: 1.5rem; border-radius: 15px; border-left: 5px solid #1383A7; margin: 1rem 0;">
    
    <h3 style="color: #1383A7;">🔵 Reconnaissance (Reconocimiento)</h3>
    <h4 style="color: #1383A7; font-size: 1.1rem;">Escaneo y Mapeo de Red</h4>
    
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
    st.markdown("## 📊 Entendiendo las Métricas del Sistema")
    
    st.markdown("""
    <div style="background: rgba(103, 58, 183, 0.1); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0;">
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            El sistema muestra diferentes tipos de métricas para ayudarte a entender la calidad 
            de las detecciones y el rendimiento. Aquí te explicamos cada una en términos simples.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para métricas
    tab_int, tab_rend = st.tabs(["📐 Métricas Internas", "⚡ Métricas de Rendimiento"])
    
    with tab_int:
        st.markdown("### 📐 Métricas Internas (Calidad de Agrupamiento)")
        
        st.write("""
        Estas métricas evalúan qué tan bien el modelo ha agrupado o separado los datos. 
        Son especialmente útiles para modelos como K-MEANS.
        """)
        
        # Silhouette Score
        st.success("🟢 **Silhouette Score (Coeficiente de Silueta)**")
        
        st.write("**¿Qué mide?**")
        st.write("""
        Qué tan bien está cada punto asignado a su cluster. Mide si los puntos están más cerca 
        de su propio grupo que de otros grupos.
        """)
        
        st.write("**💡 Analogía:**")
        st.write("""
        Imagina grupos de amigos en una fiesta. Un Silhouette alto significa que cada grupo 
        está claramente separado (amigos cerca entre sí, grupos alejados). Un Silhouette bajo 
        significa que los grupos están mezclados.
        """)
        
        st.write("**📊 Cómo interpretar:**")
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write("- **+1**: Perfecto ✅")
            st.write("- **0.7 a 1.0**: Excelente 🌟")
            st.write("- **0.5 a 0.7**: Buena separación ✅")
        with col2:
            st.write("- **0.25 a 0.5**: Razonable ⚠️")
            st.write("- **< 0.25**: Mala separación ❌")
            st.write("- **Negativo**: Muy malo ⛔")
        
        st.divider()
        
        # Calinski-Harabasz
        st.info("🔵 **Calinski-Harabasz Index**")
        
        st.write("**¿Qué mide?**")
        st.write("""
        La relación entre la separación entre clusters y la compacidad dentro de cada cluster. 
        **Valores más altos = mejor agrupamiento.**
        """)
        
        st.write("**💡 Analogía:**")
        st.write("""
        Mide qué tan "apretados" están los grupos internamente y qué tan "separados" están 
        entre sí. Como islas bien definidas en el océano vs. archipiélagos confusos.
        """)
        
        st.write("**📊 Cómo interpretar:**")
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write("- **> 1000**: Excelente ✅")
            st.write("- **500 - 1000**: Bueno ✅")
        with col2:
            st.write("- **100 - 500**: Aceptable ⚠️")
            st.write("- **< 100**: Pobre ❌")
        
        st.warning("📌 **Nota:** No tiene límite superior. En seguridad, valores > 500 indican buena separación.")
        
        st.divider()
        
        # Davies-Bouldin
        st.warning("🟠 **Davies-Bouldin Index**")
        
        st.write("**¿Qué mide?**")
        st.write("""
        La similitud promedio entre cada cluster y su cluster más similar. 
        **⚠️ Valores MÁS BAJOS son MEJORES** (inverso a las otras métricas).
        """)
        
        st.write("**💡 Analogía:**")
        st.write("""
        Mide qué tan confundibles son los grupos entre sí. Un valor bajo significa que 
        cada grupo es único y distintivo. Un valor alto significa que los grupos se parecen mucho.
        """)
        
        st.write("**📊 Cómo interpretar:**")
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.write("- **0**: Perfecto (teórico) ✅")
            st.write("- **0 - 0.5**: Excelente 🌟")
            st.write("- **0.5 - 1.0**: Bueno ✅")
        with col2:
            st.write("- **1.0 - 2.0**: Aceptable ⚠️")
            st.write("- **> 2.0**: Malo ❌")
        
        st.error("⚠️ **Importante:** Menor es mejor. Valores > 2 indican confusión entre tráfico normal y ataques.")
        
        st.divider()
        
        # Combinación de métricas
        st.subheader("🎯 Combinando las Tres Métricas")
        
        st.write("Para una evaluación completa, observa las tres métricas juntas:")
        
        st.success("""
        **✅ EXCELENTE:**  
        Silhouette > 0.5 + Calinski > 500 + Davies < 1.0
        """)
        
        st.warning("""
        **⚠️ ACEPTABLE:**  
        Silhouette > 0.3 + Calinski > 200 + Davies < 2.0
        """)
        
        st.error("""
        **❌ POBRE:**  
        Silhouette < 0.3 o Calinski < 100 o Davies > 2.5
        """)
    
    with tab_rend:
        st.markdown("### ⚡ Métricas de Rendimiento del Sistema")
        
        st.write("""
        Estas métricas te muestran cómo está funcionando tu sistema en términos de recursos 
        computacionales. Son importantes para asegurar que el IDS no sobrecargue tus dispositivos.
        """)
        
        # Grid de métricas de rendimiento (2 columnas)
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.info("🖥️ **% CPU (Procesador)**")
            st.write("**¿Qué mide?**")
            st.write("El porcentaje del procesador que está usando el sistema para hacer los análisis.")
            
            st.write("**💡 Analogía:**")
            st.write("Como el porcentaje de tu cerebro que usas para una tarea. Si usas el 100%, no puedes hacer nada más al mismo tiempo.")
            
            st.write("**📊 Valores típicos:**")
            st.write("- **0-30%**: Bajo uso, óptimo ✅")
            st.write("- **30-70%**: Uso moderado ⚠️")
            st.write("- **70-90%**: Uso alto ⚠️")
            st.write("- **> 90%**: Sobrecarga ❌")
        
        with col2:
            st.info("💾 **% Memoria (RAM)**")
            st.write("**¿Qué mide?**")
            st.write("El porcentaje de memoria RAM que está usando el sistema.")
            
            st.write("**💡 Analogía:**")
            st.write("Como el espacio en tu escritorio. Si está muy lleno, es difícil trabajar en nuevas tareas.")
            
            st.write("**📊 Valores típicos:**")
            st.write("- **0-50%**: Uso saludable ✅")
            st.write("- **50-75%**: Uso moderado ⚠️")
            st.write("- **75-90%**: Uso alto ⚠️")
            st.write("- **> 90%**: Memoria casi llena ❌")
        
        st.divider()
        
        col3, col4 = st.columns(2, gap="medium")
        
        with col3:
            st.warning("📀 **% Disco (Almacenamiento)**")
            st.write("**¿Qué mide?**")
            st.write("El porcentaje del disco duro que está ocupado.")
            
            st.write("**💡 Analogía:**")
            st.write("Como el espacio en tu armario. Si está lleno, no puedes guardar más cosas.")
            
            st.write("**📊 Valores típicos:**")
            st.write("- **0-70%**: Espacio suficiente ✅")
            st.write("- **70-85%**: Considerar limpieza ⚠️")
            st.write("- **85-95%**: Poco espacio ⚠️")
            st.write("- **> 95%**: Crítico ❌")
        
        with col4:
            st.success("⏱️ **Tiempo (segundos)**")
            st.write("**¿Qué mide?**")
            st.write("Cuánto tiempo tardó el modelo en analizar los datos y hacer la predicción.")
            
            st.write("**💡 Importancia:**")
            st.write("Para detección en tiempo real, necesitas tiempos bajos para responder rápidamente.")
            
            st.write("**📊 Valores típicos (1000 paquetes):**")
            st.write("- **< 2s**: Muy rápido ✅")
            st.write("- **2-5s**: Rápido ✅")
            st.write("- **5-10s**: Aceptable ⚠️")
            st.write("- **> 10s**: Lento ❌")
        
        st.divider()
        
        # Tabla comparativa
        st.subheader("⚙️ Comparación entre Modelos")
        
        # Crear tabla con pandas
        import pandas as pd
        
        comparacion = pd.DataFrame({
            "Modelo": ["IForest", "OCSVM", "K-MEANS", "Autoencoder"],
            "Velocidad": ["⚡⚡⚡ Muy rápido", "⚡⚡ Rápido", "⚡⚡ Rápido", "⚡ Moderado"],
            "Uso CPU": ["✅ Bajo", "⚠️ Moderado", "✅ Bajo", "⚠️ Alto"],
            "Uso RAM": ["✅ Bajo", "⚠️ Moderado", "✅ Bajo", "⚠️ Alto"]
        })
        
        st.dataframe(comparacion, use_container_width=True, hide_index=True)

    # ==================== GUÍA DE USO PASO A PASO ====================
    
    st.markdown("---")
    st.markdown("## 📖 Guía de Uso Paso a Paso")
    
    steps = [
        {
            "icon": "🔌",
            "title": "Paso 1: Seleccionar Modelo",
            "description": "En el Panel de Control, elige el modelo de detección que deseas usar.",
            "details": [
                "**IForest**: Para detección rápida y general",
                "**OCSVM**: Para alta precisión con recursos moderados",
                "**K-MEANS**: Para clasificar tipos específicos de ataques",
                "**Autoencoder**: Para máxima precisión y detección avanzada"
            ],
            "tip": "Si no estás seguro, comienza con IForest para una evaluación rápida, luego usa Autoencoder para análisis detallado."
        },
        {
            "icon": "📊",
            "title": "Paso 2: Seleccionar Tipo de Métrica",
            "description": "Elige qué métricas quieres ver para evaluar el modelo.",
            "details": [
                "**Internas**: Silhouette, Calinski, Davies (para evaluar calidad de agrupamiento)",
                "**Externas**: Requiere datos etiquetados para comparar con valores reales"
            ],
            "tip": "Para uso normal, selecciona 'Internas'. Solo usa 'Externas' si tienes un dataset con etiquetas conocidas."
        },
        {
            "icon": "📡",
            "title": "Paso 3: Capturar Paquetes",
            "description": "Decide entre captura manual o automática según tus necesidades.",
            "details": [
                "**Manual**: Tú controlas cuándo iniciar y detener",
                "**Automática**: El sistema captura periódicamente según el intervalo configurado",
                "Puedes configurar: número de paquetes, duración, intervalos"
            ],
            "tip": "Para monitoreo continuo, usa captura automática. Para análisis puntuales, usa manual."
        },
        {
            "icon": "🖱️",
            "title": "Paso 4: Realizar Predicción",
            "description": "Haz clic en '🚀 Realizar Predicción' para analizar los datos capturados.",
            "details": [
                "El modelo procesará los paquetes capturados",
                "Verás resultados en tiempo real",
                "Se generarán gráficos y estadísticas automáticamente"
            ],
            "tip": "Espera a que la captura termine antes de realizar la predicción."
        },
        {
            "icon": "📊",
            "title": "Paso 5: Interpretar Resultados",
            "description": "Revisa los gráficos, métricas y clasificaciones.",
            "details": [
                "**Gráfico de torta**: Distribución porcentual de clases",
                "**Gráfico de barras**: Cantidad de cada tipo de tráfico",
                "**Métricas**: Calidad del agrupamiento y rendimiento",
                "**Patrón de tráfico**: Visualización temporal de anomalías"
            ],
            "tip": "Si ves muchas anomalías o ataques, verifica primero si son falsos positivos antes de tomar acciones drásticas."
        },
        {
            "icon": "📄",
            "title": "Paso 6: Generar Reporte",
            "description": "Descarga un reporte PDF con todos los detalles del análisis.",
            "details": [
                "Incluye resumen ejecutivo",
                "Gráficos y estadísticas",
                "Descripción de amenazas detectadas",
                "Recomendaciones de seguridad"
            ],
            "tip": "Guarda los reportes para llevar un historial y poder comparar el comportamiento de tu red a lo largo del tiempo."
        }
    ]
    
    for idx, step in enumerate(steps, 1):
        color_map = {
            1: "#10B981",
            2: "#1383A7",
            3: "#F59E0B",
            4: "#104E63",
            5: "#EF4444",
            6: "#1383A7"
        }
        color = color_map.get(idx, "#0C4A6E")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid {color}; margin: 1rem 0;">
            <h3 style="color: {color}; margin-top: 0;">
                <span style="font-size: 2rem; margin-right: 0.5rem;">{step['icon']}</span>
                {step['title']}
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
                {step['description']}
            </p>
            <ul style="font-size: 1.05rem; line-height: 1.7; margin-left: 1.5rem;">
                {''.join([f'<li>{detail}</li>' for detail in step['details']])}
            </ul>
            <div style="background: rgba(255, 235, 59, 0.15); padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 3px solid #FFC107;">
                <strong style="color: #F57F17;">💡 Consejo:</strong> {step['tip']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==================== PREGUNTAS FRECUENTES ====================
    
    st.markdown("---")
    st.markdown("## ❓ Preguntas Frecuentes (FAQ)")
    
    with st.expander("❓ ¿Qué tan preciso es el sistema?", expanded=False):
        st.markdown("""
        La precisión depende del modelo seleccionado y de la calidad de los datos de entrenamiento:
        
        - **IForest y OCSVM**: ~85-95% de precisión en detección binaria (normal vs anómalo)
        - **K-MEANS**: ~80-90% en clasificación multiclase
        - **Autoencoder**: ~90-98% con el modelo entrenado correctamente
        
        Los factores que afectan la precisión incluyen:
        - Calidad de los datos de captura
        - Variabilidad del tráfico normal en tu red específica
        - Tipos de ataques (algunos son más fáciles de detectar que otros)
        - Configuración de parámetros del modelo
        """)
    
    with st.expander("❓ ¿Cuántos paquetes debo capturar?", expanded=False):
        st.markdown("""
        Depende de tu objetivo:
        
        - **Pruebas rápidas**: 100-500 paquetes (2-5 segundos de tráfico)
        - **Análisis estándar**: 1,000-5,000 paquetes (1-3 minutos)
        - **Análisis profundo**: 10,000+ paquetes (5+ minutos)
        - **Monitoreo continuo**: Capturas automáticas cada 5-10 minutos
        
        💡 **Recomendación**: Comienza con 1,000 paquetes. Si tu red es muy activa, 
        podrías necesitar menos; si es tranquila, captura más para tener datos suficientes.
        """)
    
    with st.expander("❓ ¿Qué hago si detecto un ataque?", expanded=False):
        st.markdown("""
        Sigue estos pasos:
        
        1. **No entres en pánico**: Verifica primero si es un falso positivo
        2. **Confirma la amenaza**:
           - Ejecuta el análisis con otro modelo
           - Revisa las IPs de origen en los datos capturados
           - Verifica si los patrones son consistentes
        
        3. **Acciones inmediatas** según el tipo de ataque:
           - **DDoS**: Activa rate limiting, bloquea IPs ofensoras
           - **Reconnaissance**: Restringe respuestas, habilita logging detallado
        
        4. **Documenta todo**:
           - Descarga el reporte PDF
           - Guarda los datos capturados en CSV
           - Anota fecha, hora y circunstancias
        
        5. **Monitoreo continuo**: Activa captura automática para vigilar si el ataque persiste
        """)
    
    with st.expander("❓ ¿Puedo usar múltiples modelos a la vez?", expanded=False):
        st.markdown("""
        Sí, y es muy recomendable. Ve a la página **"Comparar Modelos"** donde puedes:
        
        - ✅ Ejecutar varios modelos sobre los mismos datos simultáneamente
        - ✅ Comparar resultados lado a lado
        - ✅ Ver qué modelo es más confiable para tu tipo de red
        - ✅ Identificar consenso entre modelos (si 3/4 modelos coinciden, es más confiable)
        
        💡 **Mejor práctica**: Usa IForest para detección rápida, luego confirma con 
        Autoencoder para alta precisión.
        """)
    
    with st.expander("❓ ¿El sistema puede detectar ataques nuevos (zero-day)?", expanded=False):
        st.markdown("""
        **Parcialmente**, depende del modelo:
        
        - **IForest y OCSVM**: ✅ Sí, pueden detectar patrones anómalos nunca vistos (son modelos de detección de anomalías)
        - **K-MEANS**: ⚠️ Limitado, solo detecta si el ataque se agrupa de forma diferente
        - **Autoencoder**: ✅ Sí, mediante el error de reconstrucción puede identificar patrones completamente nuevos
        
        Sin embargo:
        - No clasificarán el tipo específico si es un ataque totalmente nuevo
        - Aparecerán como "Anómalo" o podrían caer en categorías conocidas similares
        - El Autoencoder es el mejor para esto gracias a su capacidad de reconstrucción
        """)
    
    with st.expander("❓ ¿Afectará el rendimiento de mi red?", expanded=False):
        st.markdown("""
        **No**, el sistema solo "escucha" el tráfico pasivamente:
        
        - ✅ No intercepta ni modifica paquetes
        - ✅ No añade latencia a las comunicaciones
        - ✅ Solo consume recursos en el dispositivo donde se ejecuta (CPU, RAM)
        - ✅ El consumo de ancho de banda es mínimo (solo lectura)
        
        **Impacto típico**:
        - CPU: 5-30% durante análisis activo
        - RAM: 200-800 MB dependiendo del modelo y cantidad de datos
        - Red: < 1% del ancho de banda disponible
        
        💡 **Recomendación**: Ejecuta el sistema en un dispositivo dedicado (ej: Raspberry Pi) 
        para no afectar otros servicios.
        """)

    # ==================== CONSEJOS Y MEJORES PRÁCTICAS ====================
    
    st.markdown("---")
    st.markdown("## 💡 Consejos y Mejores Prácticas")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 100%;">
            <h3 style="color: #10B981;">✅ Buenas Prácticas</h3>
            <ul style="font-size: 1.05rem; line-height: 1.8;">
                <li><strong>Establece una línea base</strong>: Ejecuta el sistema durante varios días en tráfico normal para entender qué es "normal" en tu red</li>
                <li><strong>Monitoreo regular</strong>: Configura capturas automáticas para vigilancia continua</li>
                <li><strong>Compara modelos</strong>: No te fíes de un solo modelo, usa la función de comparación</li>
                <li><strong>Guarda reportes</strong>: Mantén un histórico de análisis para detectar tendencias</li>
                <li><strong>Ajusta umbrales</strong>: Usa las opciones de desarrollador para afinar la sensibilidad</li>
                <li><strong>Actualiza modelos</strong>: Re-entrena periódicamente con datos nuevos de tu red</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 12px; height: 100%;">
            <h3 style="color: #EF4444;">❌ Errores Comunes</h3>
            <ul style="font-size: 1.05rem; line-height: 1.8;">
                <li><strong>Capturar muy pocos datos</strong>: < 100 paquetes no son representativos</li>
                <li><strong>Ignorar el contexto</strong>: Una "anomalía" puede ser simplemente un patrón nuevo legítimo</li>
                <li><strong>No verificar falsos positivos</strong>: Siempre confirma antes de bloquear IPs</li>
                <li><strong>Usar un solo modelo</strong>: Diferentes modelos tienen diferentes fortalezas</li>
                <li><strong>No monitorear recursos</strong>: Vigila el uso de CPU/RAM para evitar sobrecargas</li>
                <li><strong>Olvidar documentar</strong>: Descarga y guarda los reportes para análisis posterior</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==================== FOOTER DE LA GUÍA ====================
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #0C4A6E 0%, #1383A7 100%); 
                border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">🎓 ¡Felicitaciones!</h2>
        <p style="color: #F0FAFE; font-size: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem;">
            Ahora tienes todo el conocimiento necesario para usar este sistema de detección de intrusiones 
            de manera efectiva y proteger tu red IoT.
        </p>
        <p style="color: white; font-size: 1.1rem;">
            🚀 <strong>Estás listo para comenzar. ¡Ve al Panel de Control y empieza a proteger tu red!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

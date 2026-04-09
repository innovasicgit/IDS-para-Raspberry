"""
Módulo de explicaciones inteligentes para resultados de predicción.
Genera análisis contextualizados según los datos obtenidos.
"""

import numpy as np

from backend.notifications import get_alert_level_from_anomaly_percentage


def explicar_distribucion(labels, values, model_option):
    """
    Genera una explicación inteligente de la distribución de resultados.
    
    Args:
        labels: Lista de etiquetas (Normal, Anómalo, DDOS_TCP, etc.)
        values: Lista de valores correspondientes
        model_option: Modelo usado (IForest, OCSVM, KMEANS, AUTOENCODER)
    
    Returns:
        str: Explicación detallada de la distribución
    """
    total = sum(values)
    if total == 0:
        return "⚠️ No se detectaron paquetes para analizar."
    
    # Crear diccionario de porcentajes
    distribuciones = {}
    for label, value in zip(labels, values):
        porcentaje = (value / total) * 100
        distribuciones[label] = {'cantidad': value, 'porcentaje': porcentaje}
    
    # Análisis según el tipo de modelo
    if model_option in ['IForest', 'OCSVM']:
        # Modelos binarios: Normal vs Anómalo
        normal = distribuciones.get('Normal', {'cantidad': 0, 'porcentaje': 0})
        anomalo = distribuciones.get('Anómalo', {'cantidad': 0, 'porcentaje': 0})
        
        explicacion = f"### 🔍 Análisis de la Distribución\n\n"

        # Unificar con los umbrales oficiales de alerta (backend.notifications).
        anomaly_pct = float(anomalo['porcentaje'])
        alert_level = get_alert_level_from_anomaly_percentage(anomaly_pct)

        if alert_level == 'normal':
            explicacion += f"✅ **Estado: NORMAL**\n\n"
            explicacion += (
                f"Se detectó **{anomaly_pct:.1f}% de tráfico anómalo** ({anomalo['cantidad']:,} paquetes) y "
                f"**{normal['porcentaje']:.1f}% de tráfico normal** ({normal['cantidad']:,} paquetes). "
                f"Este nivel está dentro del margen definido por el sistema para operación normal.\n\n"
                f"💡 **Recomendación:** Mantener monitoreo regular y revisar anomalías si se repiten."
            )
        elif alert_level == 'suspicious':
            explicacion += f"⚠️ **Estado: SOSPECHOSO - REQUIERE ATENCIÓN**\n\n"
            explicacion += (
                f"Se detectó **{anomaly_pct:.1f}% de tráfico anómalo** ({anomalo['cantidad']:,} paquetes), "
                f"lo cual supera el umbral de operación normal. Esto podría indicar:\n"
                f"- Tráfico legítimo pero inusual (picos, actualizaciones)\n"
                f"- Reconocimiento/escaneo\n"
                f"- Actividad sospechosa inicial\n\n"
                f"⚠️ **Recomendación:** Investigar los paquetes anómalos y reforzar reglas de seguridad."
            )
        else:
            explicacion += f"🚨 **Estado: CRÍTICO - ACCIÓN INMEDIATA REQUERIDA**\n\n"
            explicacion += (
                f"¡ALERTA! Se detectó **{anomaly_pct:.1f}% de tráfico anómalo** ({anomalo['cantidad']:,} paquetes). "
                f"Este nivel sugiere un evento severo o ataque activo.\n\n"
                f"🚨 **ACCIÓN INMEDIATA:**\n"
                f"1. Aislar dispositivos sospechosos de la red\n"
                f"2. Revisar firewall y reglas de seguridad\n"
                f"3. Contactar al equipo de seguridad\n"
                f"4. Considerar resetear contraseñas y credenciales"
            )
    
    elif model_option in ['KMEANS', 'AUTOENCODER']:
        # Modelos multiclase: Normal, DDOS_TCP, DDOS_UDP, Reconnaissance
        normal = distribuciones.get('Normal', {'cantidad': 0, 'porcentaje': 0})
        ddos_tcp = distribuciones.get('DDOS_TCP', {'cantidad': 0, 'porcentaje': 0})
        ddos_udp = distribuciones.get('DDOS_UDP', {'cantidad': 0, 'porcentaje': 0})
        recon = distribuciones.get('Reconnaissance', {'cantidad': 0, 'porcentaje': 0})
        
        ataques_totales = ddos_tcp['cantidad'] + ddos_udp['cantidad'] + recon['cantidad']
        porcentaje_ataques = (ataques_totales / total) * 100
        
        explicacion = f"### 🔍 Análisis Detallado de Amenazas\n\n"

        # Unificar con los umbrales oficiales de alerta.
        alert_level = get_alert_level_from_anomaly_percentage(porcentaje_ataques)
        if alert_level == 'normal':
            explicacion += f"✅ **Estado: NORMAL**\n\n"
            explicacion += (
                f"Se detectó **{porcentaje_ataques:.1f}%** de tráfico asociado a amenazas "
                f"({ataques_totales:,} paquetes). Este nivel está dentro del margen definido por el sistema.\n\n"
            )
        elif alert_level == 'suspicious':
            explicacion += f"⚠️ **Estado: SOSPECHOSO - AMENAZAS DETECTADAS**\n\n"
            explicacion += (
                f"Se identificaron **{ataques_totales:,} paquetes** ({porcentaje_ataques:.1f}% del total). "
                f"Se recomienda análisis y mitigación.\n\n"
            )
        else:
            explicacion += f"🚨 **Estado: CRÍTICO - ATAQUE EN CURSO**\n\n"
            explicacion += (
                f"¡ALERTA! **{porcentaje_ataques:.1f}%** del tráfico es malicioso "
                f"({ataques_totales:,} paquetes). Acción inmediata requerida.\n\n"
            )
        
        # Explicar cada tipo de ataque detectado
        if ddos_tcp['cantidad'] > 0:
            explicacion += f"#### 🔴 DDoS TCP ({ddos_tcp['cantidad']:,} paquetes - {ddos_tcp['porcentaje']:.1f}%)\n"
            explicacion += f"**¿Qué es?** Ataque de denegación de servicio usando protocolo TCP. El atacante envía múltiples "
            explicacion += f"solicitudes de conexión (SYN flood) para saturar el servidor.\n\n"
            explicacion += f"**Impacto:** Puede dejar el servidor inaccesible, ralentizar servicios web/aplicaciones.\n\n"
            explicacion += f"**Recomendación:**\n"
            explicacion += f"- Activar protección SYN cookies\n"
            explicacion += f"- Implementar rate limiting en el firewall\n"
            explicacion += f"- Considerar usar CloudFlare o servicio anti-DDoS\n\n"
        
        if ddos_udp['cantidad'] > 0:
            explicacion += f"#### 🟠 DDoS UDP ({ddos_udp['cantidad']:,} paquetes - {ddos_udp['porcentaje']:.1f}%)\n"
            explicacion += f"**¿Qué es?** Ataque que inunda la red con paquetes UDP (amplificación DNS, NTP).\n\n"
            explicacion += f"**Impacto:** Saturación del ancho de banda, red lenta o inaccesible.\n\n"
            explicacion += f"**Recomendación:**\n"
            explicacion += f"- Bloquear puertos UDP no utilizados\n"
            explicacion += f"- Filtrar tráfico UDP entrante sospechoso\n"
            explicacion += f"- Verificar configuración de DNS/NTP\n\n"
        
        if recon['cantidad'] > 0:
            explicacion += f"#### 🔵 Reconnaissance ({recon['cantidad']:,} paquetes - {recon['porcentaje']:.1f}%)\n"
            explicacion += f"**¿Qué es?** Escaneo de red para identificar servicios, puertos abiertos y vulnerabilidades. "
            explicacion += f"Es la fase previa a un ataque.\n\n"
            explicacion += f"**Impacto:** El atacante está mapeando tu red para planear un ataque futuro.\n\n"
            explicacion += f"**Recomendación:**\n"
            explicacion += f"- Bloquear IPs origen del escaneo\n"
            explicacion += f"- Cerrar puertos innecesarios\n"
            explicacion += f"- Activar detección de escaneos en el firewall\n"
            explicacion += f"- Mantenerse alerta: un ataque podría venir pronto\n\n"
        
        if normal['porcentaje'] > 50:
            explicacion += f"💡 **Nota:** Aunque se detectaron amenazas, el {normal['porcentaje']:.1f}% del tráfico sigue siendo normal, "
            explicacion += f"lo que sugiere que los ataques son selectivos o están en fase inicial."
    
    return explicacion


def explicar_metricas_rendimiento(tiempo, cpu, memoria, disco):
    """
    Genera explicación inteligente de las métricas de rendimiento.
    
    Args:
        tiempo: Tiempo de ejecución en segundos
        cpu: Porcentaje de uso de CPU
        memoria: Porcentaje de uso de memoria
        disco: Porcentaje de uso de disco
    
    Returns:
        str: Explicación de las métricas
    """
    explicacion = "### ⚙️ Interpretación de Métricas de Rendimiento\n\n"
    
    # Análisis del tiempo
    if tiempo < 1:
        explicacion += f"⚡ **Tiempo de predicción: EXCELENTE** ({tiempo:.2f}s)\n"
        explicacion += f"El análisis fue extremadamente rápido. Ideal para detección en tiempo real.\n\n"
    elif tiempo < 5:
        explicacion += f"✅ **Tiempo de predicción: BUENO** ({tiempo:.2f}s)\n"
        explicacion += f"Tiempo aceptable para análisis en tiempo real.\n\n"
    elif tiempo < 15:
        explicacion += f"⚠️ **Tiempo de predicción: MODERADO** ({tiempo:.2f}s)\n"
        explicacion += f"El análisis tomó algo de tiempo. Podría ser mejorable con optimización.\n\n"
    else:
        explicacion += f"🐌 **Tiempo de predicción: LENTO** ({tiempo:.2f}s)\n"
        explicacion += f"El análisis tomó considerable tiempo. Considere reducir el dataset o optimizar el modelo.\n\n"
    
    # Análisis de CPU
    if cpu < 30:
        explicacion += f"🖥️ **CPU: USO BAJO** ({cpu:.1f}%)\n"
        explicacion += f"El sistema tiene recursos disponibles. Puede manejar más carga sin problemas.\n\n"
    elif cpu < 60:
        explicacion += f"🖥️ **CPU: USO MODERADO** ({cpu:.1f}%)\n"
        explicacion += f"Uso normal del procesador. El sistema está operando eficientemente.\n\n"
    elif cpu < 85:
        explicacion += f"⚠️ **CPU: USO ALTO** ({cpu:.1f}%)\n"
        explicacion += f"El procesador está bajo carga considerable. Monitorear si persiste.\n\n"
    else:
        explicacion += f"🔥 **CPU: USO CRÍTICO** ({cpu:.1f}%)\n"
        explicacion += f"¡El procesador está saturado! Otros procesos podrían ralentizarse. "
        explicacion += f"Considere cerrar aplicaciones innecesarias o distribuir la carga.\n\n"
    
    # Análisis de Memoria
    if memoria < 50:
        explicacion += f"💾 **Memoria: DISPONIBLE** ({memoria:.1f}%)\n"
        explicacion += f"Hay suficiente RAM libre. El sistema puede manejar más operaciones simultáneas.\n\n"
    elif memoria < 75:
        explicacion += f"💾 **Memoria: USO NORMAL** ({memoria:.1f}%)\n"
        explicacion += f"Uso típico de memoria. Sin problemas previstos.\n\n"
    elif memoria < 90:
        explicacion += f"⚠️ **Memoria: USO ALTO** ({memoria:.1f}%)\n"
        explicacion += f"La RAM está cerca de su límite. Considere cerrar aplicaciones no esenciales.\n\n"
    else:
        explicacion += f"🚨 **Memoria: CRÍTICA** ({memoria:.1f}%)\n"
        explicacion += f"¡RAM casi llena! El sistema podría empezar a usar swap (muy lento). "
        explicacion += f"Cierre aplicaciones urgentemente o reinicie el sistema.\n\n"
    
    # Análisis de Disco
    if disco < 70:
        explicacion += f"📀 **Disco: ESPACIO SUFICIENTE** ({disco:.1f}%)\n"
        explicacion += f"Hay espacio adecuado en el disco.\n\n"
    elif disco < 85:
        explicacion += f"📀 **Disco: CONSIDERAR LIMPIEZA** ({disco:.1f}%)\n"
        explicacion += f"El disco está llegando a su capacidad. Considere eliminar archivos temporales o logs antiguos.\n\n"
    else:
        explicacion += f"⚠️ **Disco: ESPACIO LIMITADO** ({disco:.1f}%)\n"
        explicacion += f"¡Disco casi lleno! Elimine archivos innecesarios para evitar problemas de rendimiento.\n\n"
    
    # Resumen general
    problemas = []
    if cpu >= 85:
        problemas.append("CPU saturada")
    if memoria >= 85:
        problemas.append("Memoria crítica")
    if disco >= 85:
        problemas.append("Disco casi lleno")
    
    if problemas:
        explicacion += f"🚨 **Alertas:** {', '.join(problemas)}. Tome medidas correctivas.\n"
    else:
        explicacion += f"✅ **Resumen:** El sistema está operando dentro de parámetros normales.\n"
    
    return explicacion


def explicar_patron_trafico(datos_para_grafica):
    """
    Analiza el patrón de tráfico y genera una explicación inteligente.
    
    Args:
        datos_para_grafica: DataFrame con los datos de tráfico
    
    Returns:
        str: Explicación del patrón de tráfico
    """
    try:
        numeric_data = datos_para_grafica.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return ""
        
        traffic_data = numeric_data.mean(axis=1)
        
        # Calcular estadísticas
        promedio = traffic_data.mean()
        std = traffic_data.std()
        maximo = traffic_data.max()
        minimo = traffic_data.min()
        
        # Detectar picos (valores > 2 desviaciones estándar)
        umbral_pico = promedio + (2 * std)
        picos = (traffic_data > umbral_pico).sum()
        porcentaje_picos = (picos / len(traffic_data)) * 100
        
        # Calcular variabilidad
        coef_variacion = (std / promedio) * 100 if promedio > 0 else 0
        
        explicacion = "### 📊 Análisis del Patrón de Tráfico\n\n"
        
        # Interpretación general
        if coef_variacion < 20:
            explicacion += f"✅ **Patrón: ESTABLE Y UNIFORME**\n\n"
            explicacion += f"El tráfico de red muestra un comportamiento muy consistente (variabilidad: {coef_variacion:.1f}%). "
            explicacion += f"Esto es típico de redes corporativas o domésticas durante operación normal.\n\n"
        elif coef_variacion < 50:
            explicacion += f"📊 **Patrón: VARIABILIDAD MODERADA**\n\n"
            explicacion += f"El tráfico presenta fluctuaciones normales (variabilidad: {coef_variacion:.1f}%). "
            explicacion += f"Comportamiento esperado con actividad web, streaming o descargas.\n\n"
        else:
            explicacion += f"⚠️ **Patrón: ALTAMENTE VARIABLE**\n\n"
            explicacion += f"El tráfico muestra gran irregularidad (variabilidad: {coef_variacion:.1f}%). "
            explicacion += f"Podría indicar ráfagas de actividad inusual o ataques intermitentes.\n\n"
        
        # Análisis de picos
        if porcentaje_picos < 1:
            explicacion += f"✅ **Picos anómalos:** Muy pocos ({picos} picos, {porcentaje_picos:.1f}%)\n"
            explicacion += f"No se detectaron ráfagas significativas de tráfico.\n\n"
        elif porcentaje_picos < 5:
            explicacion += f"⚠️ **Picos anómalos:** Algunos detectados ({picos} picos, {porcentaje_picos:.1f}%)\n"
            explicacion += f"Se observaron algunas ráfagas de tráfico. Podrían ser descargas grandes, "
            explicacion += f"actualizaciones de software o actividad inusual.\n\n"
        else:
            explicacion += f"🚨 **Picos anómalos:** FRECUENTES ({picos} picos, {porcentaje_picos:.1f}%)\n"
            explicacion += f"¡Múltiples ráfagas de tráfico detectadas! Esto podría indicar:\n"
            explicacion += f"- Ataque DDoS en curso\n"
            explicacion += f"- Escaneo masivo de puertos\n"
            explicacion += f"- Dispositivo comprometido enviando spam/malware\n\n"
        
        # Interpretación de las líneas de la gráfica
        explicacion += f"#### 📈 Interpretación de la Gráfica:\n\n"
        explicacion += f"- **Línea azul (Tráfico):** Muestra la intensidad promedio del tráfico en cada muestra analizada.\n"
        explicacion += f"- **Línea verde punteada (Techo):** Límite superior esperado. Picos por encima sugieren anomalías.\n"
        explicacion += f"- **Línea naranja punteada (Suelo):** Límite inferior. Caídas abruptas podrían indicar problemas.\n\n"
        
        # Recomendaciones
        if porcentaje_picos >= 5 or coef_variacion >= 50:
            explicacion += f"💡 **Recomendación:** Investigar los picos de tráfico. Revise los dispositivos conectados "
            explicacion += f"y verifique logs del router/firewall para identificar la fuente.\n"
        
        return explicacion
        
    except Exception:
        return ""


def generar_resumen_general(resumen_prediccion, metricas_rendimiento, model_option, tiene_patron=False):
    """
    Genera un resumen ejecutivo completo de toda la predicción.
    
    Args:
        resumen_prediccion: Dict con labels y values
        metricas_rendimiento: Dict con tiempo, cpu, memoria, disco
        model_option: Modelo usado
        tiene_patron: Boolean indicando si hay gráfica de patrón
    
    Returns:
        str: Resumen ejecutivo completo
    """
    labels = resumen_prediccion['labels']
    values = resumen_prediccion['values']
    total = sum(values)
    
    resumen = "## 📋 Resumen Ejecutivo de la Predicción\n\n"
    resumen += "---\n\n"
    
    # 1. Datos analizados
    resumen += f"### 📊 Volumen de Datos\n"
    resumen += f"- **Total de paquetes analizados:** {total:,}\n"
    resumen += f"- **Modelo de detección:** {model_option}\n"
    resumen += f"- **Tiempo de procesamiento:** {metricas_rendimiento['tiempo']:.2f} segundos\n\n"
    
    # 2. Veredicto general (unificado con umbrales oficiales)
    if model_option in ['IForest', 'OCSVM']:
        anomaly_pct = 0.0
        if 'Anómalo' in labels:
            anomaly_pct = (values[labels.index('Anómalo')] / total * 100) if total > 0 else 0
        alert_level = get_alert_level_from_anomaly_percentage(anomaly_pct)
        if alert_level == 'normal':
            resumen += f"### ✅ VEREDICTO: NIVEL NORMAL\n\n"
            resumen += f"Se detectó {anomaly_pct:.1f}% de anomalías. Está dentro del margen definido para operación normal.\n\n"
        elif alert_level == 'suspicious':
            resumen += f"### ⚠️ VEREDICTO: ACTIVIDAD SOSPECHOSA\n\n"
            resumen += f"Se detectó {anomaly_pct:.1f}% de anomalías, superando el umbral de normalidad. Requiere revisión.\n\n"
        else:
            resumen += f"### 🚨 VEREDICTO: SITUACIÓN CRÍTICA\n\n"
            resumen += f"¡ALERTA! {anomaly_pct:.1f}% del tráfico es anómalo. Se requiere acción inmediata.\n\n"
    else:
        # Modelos multiclase
        ataques = sum([v for l, v in zip(labels, values) if l != 'Normal'])
        pct_ataques = (ataques / total * 100) if total > 0 else 0
        alert_level = get_alert_level_from_anomaly_percentage(pct_ataques)
        if alert_level == 'normal':
            resumen += f"### ✅ VEREDICTO: NIVEL NORMAL\n\n"
            resumen += f"Se detectó {pct_ataques:.1f}% de tráfico malicioso. Está dentro del margen definido por el sistema.\n\n"
        elif alert_level == 'suspicious':
            resumen += f"### ⚠️ VEREDICTO: AMENAZAS DETECTADAS\n\n"
            resumen += f"Se identificaron {ataques:,} paquetes maliciosos ({pct_ataques:.1f}%). Requiere atención.\n\n"
        else:
            resumen += f"### 🚨 VEREDICTO: ATAQUE EN CURSO\n\n"
            resumen += f"¡ALERTA! {pct_ataques:.1f}% del tráfico es malicioso ({ataques:,} paquetes). Acción urgente requerida.\n\n"
    
    # 3. Hallazgos clave
    resumen += f"### 🔍 Hallazgos Clave\n\n"
    for label, value in zip(labels, values):
        pct = (value / total * 100) if total > 0 else 0
        icono = "✅" if label == "Normal" else "🚨"
        resumen += f"{icono} **{label}:** {value:,} paquetes ({pct:.1f}%)\n"
    resumen += "\n"
    
    # 4. Estado del sistema
    resumen += f"### 💻 Estado del Sistema\n\n"
    cpu_status = "✅ Normal" if metricas_rendimiento['cpu'] < 70 else "⚠️ Alto" if metricas_rendimiento['cpu'] < 90 else "🔥 Crítico"
    mem_status = "✅ Normal" if metricas_rendimiento['memoria'] < 75 else "⚠️ Alto" if metricas_rendimiento['memoria'] < 90 else "🚨 Crítico"
    
    resumen += f"- **CPU:** {metricas_rendimiento['cpu']:.1f}% - {cpu_status}\n"
    resumen += f"- **Memoria:** {metricas_rendimiento['memoria']:.1f}% - {mem_status}\n"
    resumen += f"- **Disco:** {metricas_rendimiento['disco']:.1f}%\n\n"
    
    # 5. Patrón de tráfico (si existe)
    if tiene_patron:
        resumen += f"### 📈 Patrón de Tráfico\n\n"
        resumen += f"Se analizó el patrón temporal del tráfico. Revise la gráfica inferior para identificar "
        resumen += f"picos anómalos o comportamientos irregulares que podrían indicar ataques.\n\n"
    
    # 6. Recomendaciones finales
    resumen += f"### 💡 Recomendaciones Finales\n\n"
    
    if model_option in ['IForest', 'OCSVM']:
        anomaly_pct = 0.0
        if 'Anómalo' in labels:
            anomaly_pct = (values[labels.index('Anómalo')] / total * 100) if total > 0 else 0
        alert_level = get_alert_level_from_anomaly_percentage(anomaly_pct)
        if alert_level == 'normal':
            resumen += f"- Continuar con el monitoreo regular\n"
            resumen += f"- Mantener las defensas actuales\n"
            resumen += f"- Revisar logs periódicamente\n"
        elif alert_level == 'suspicious':
            resumen += f"- Investigar paquetes anómalos en detalle\n"
            resumen += f"- Verificar configuración de firewall\n"
            resumen += f"- Identificar dispositivos sospechosos\n"
            resumen += f"- Aumentar frecuencia de monitoreo\n"
        else:
            resumen += f"- 🚨 **ACCIÓN INMEDIATA:** Aislar segmentos comprometidos\n"
            resumen += f"- Bloquear IPs maliciosas identificadas\n"
            resumen += f"- Revisar todos los dispositivos IoT\n"
            resumen += f"- Contactar equipo de seguridad\n"
            resumen += f"- Considerar reseteo de credenciales\n"
    else:
        resumen += f"- Revisar y bloquear las IPs origen de los ataques\n"
        resumen += f"- Implementar reglas de firewall más estrictas\n"
        resumen += f"- Activar protección anti-DDoS si está disponible\n"
        resumen += f"- Documentar el incidente para análisis futuro\n"
    
    resumen += "\n---\n\n"
    resumen += f"*Análisis generado automáticamente por el Sistema IDS*\n"
    
    return resumen

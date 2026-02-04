"""
Funciones de formateo para la UI.
"""

from typing import Union


def format_number(value: Union[int, float], decimals: int = 0) -> str:
    """
    Formatear número con separadores de miles.
    
    Args:
        value: Número a formatear
        decimals: Decimales a mostrar
        
    Returns:
        String formateado
    """
    if decimals == 0:
        return f"{int(value):,}".replace(",", ".")
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formatear valor como porcentaje.
    
    Args:
        value: Valor entre 0 y 1 (o 0 y 100)
        decimals: Decimales a mostrar
        
    Returns:
        String con formato de porcentaje
    """
    # Si el valor está entre 0 y 1, convertir a porcentaje
    if 0 <= value <= 1:
        value *= 100
    
    return f"{value:.{decimals}f}%"


def format_bytes(bytes_value: int, precision: int = 2) -> str:
    """
    Formatear bytes a formato legible (KB, MB, GB, etc.).
    
    Args:
        bytes_value: Cantidad de bytes
        precision: Decimales a mostrar
        
    Returns:
        String formateado
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    size = float(bytes_value)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.{precision}f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """
    Formatear duración en segundos a formato legible.
    
    Args:
        seconds: Duración en segundos
        
    Returns:
        String formateado (ej: "2h 30m 15s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"
    
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    if hours < 24:
        return f"{hours}h {remaining_minutes}m"
    
    days = int(hours // 24)
    remaining_hours = int(hours % 24)
    
    return f"{days}d {remaining_hours}h"


def format_attack_name(attack_type: str) -> str:
    """
    Formatear nombre de ataque para mejor legibilidad.
    
    Args:
        attack_type: Tipo de ataque (ej: "ddos_tcp", "normal")
        
    Returns:
        Nombre formateado
    """
    # Diccionario de nombres más legibles
    attack_names = {
        'normal': 'Tráfico Normal',
        'ddos_tcp': 'DDoS TCP',
        'ddos_udp': 'DDoS UDP',
        'ddos_http': 'DDoS HTTP',
        'ddos_icmp': 'DDoS ICMP',
        'portscan': 'Port Scanning',
        'bruteforce': 'Fuerza Bruta',
        'mitm': 'Man-in-the-Middle',
        'malware': 'Malware',
        'injection': 'SQL Injection',
        'xss': 'Cross-Site Scripting',
        'anomaly': 'Anomalía Detectada',
        'ransomware': 'Ransomware',
        'botnet': 'Botnet',
        'exploit': 'Exploit',
    }
    
    # Buscar en diccionario (case-insensitive)
    attack_lower = attack_type.lower()
    if attack_lower in attack_names:
        return attack_names[attack_lower]
    
    # Si no está en el diccionario, formatear: quitar guiones bajos y capitalizar
    return attack_type.replace('_', ' ').title()


def format_model_name(model_id: str) -> str:
    """
    Formatear nombre de modelo para visualización.
    
    Args:
        model_id: ID del modelo (ej: "isolation_forest")
        
    Returns:
        Nombre formateado
    """
    model_names = {
        'isolation_forest': 'Isolation Forest',
        'iforest': 'Isolation Forest',
        'one_class_svm': 'One-Class SVM',
        'ocsvm': 'One-Class SVM',
        'autoencoder': 'Autoencoder',
        'kmeans': 'K-Means',
        'dbscan': 'DBSCAN',
    }
    
    return model_names.get(model_id.lower(), model_id.replace('_', ' ').title())


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncar texto largo.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a agregar si se trunca
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_ip_address(ip: str) -> str:
    """
    Formatear dirección IP (agregar monospace).
    
    Args:
        ip: Dirección IP
        
    Returns:
        HTML formateado
    """
    return f"<code>{ip}</code>"


def format_timestamp(timestamp: Union[str, float], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formatear timestamp.
    
    Args:
        timestamp: Timestamp a formatear
        format_str: Formato de salida
        
    Returns:
        String formateado
    """
    from datetime import datetime
    
    if isinstance(timestamp, str):
        # Intentar parsear string
        try:
            dt = datetime.fromisoformat(timestamp)
        except ValueError:
            return timestamp
    else:
        # Asumir que es un timestamp Unix
        dt = datetime.fromtimestamp(timestamp)
    
    return dt.strftime(format_str)


def format_confidence(confidence: float, show_icon: bool = True) -> str:
    """
    Formatear nivel de confianza con icono.
    
    Args:
        confidence: Valor de confianza (0-1)
        show_icon: Si mostrar icono
        
    Returns:
        String formateado
    """
    percentage = format_percentage(confidence)
    
    if not show_icon:
        return percentage
    
    # Iconos basados en nivel de confianza
    if confidence >= 0.9:
        icon = "🟢"  # Alta confianza
    elif confidence >= 0.7:
        icon = "🟡"  # Media confianza
    else:
        icon = "🔴"  # Baja confianza
    
    return f"{icon} {percentage}"

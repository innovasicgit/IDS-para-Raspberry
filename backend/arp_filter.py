"""
Módulo para filtrado de paquetes ARP durante la captura de tráfico.
Permite limitar la cantidad de paquetes ARP para mejorar la calidad de datos.
"""

import pandas as pd


def apply_realtime_arp_filter(protocol, arp_count, packets_count, arp_limit_mode='low'):
    """
    Decide en tiempo real si aceptar un paquete basado en su tipo de protocolo y el filtro ARP.
    
    Parameters:
    -----------
    protocol : str
        Tipo de protocolo del paquete (e.g., 'TCP', 'UDP', 'ARP', 'ICMP')
    arp_count : int
        Cantidad de paquetes ARP aceptados hasta ahora
    packets_count : int
        Cantidad total de paquetes aceptados hasta ahora
    arp_limit_mode : str
        Modo de límite de ARP: 'low', 'medium', 'high', 'none'
        - 'low': ~15% ARP (1 ARP por cada 6-7 paquetes)
        - 'medium': ~30% ARP (1 ARP por cada 3 paquetes)
        - 'high': ~50% ARP (1 ARP por cada 2 paquetes)
        - 'none': 100% ARP (sin filtro)
    
    Returns:
    --------
    bool
        True si el paquete debe aceptarse, False si debe descartarse
    """
    # proporción máxima de ARP permitida (sobre paquetes aceptados)
    arp_ratios = {
        'low': 0.15,     # ~15% de ARP, mínimo posible
        'medium': 0.30,  # ~30% de ARP
        'high': 0.50,    # ~50% de ARP
        'none': 1.0      # sin filtro, todos los ARP pasan
    }
    
    arp_ratio = arp_ratios.get(arp_limit_mode, 0.15)
    
    # Aceptar todos en modo 'none'
    if arp_limit_mode == 'none':
        return True
    
    # Aceptar todos los paquetes que no son ARP
    if protocol != 'ARP':
        return True
    
    # Para paquetes ARP: aceptar según el ratio
    # calcular ratio usando paquetes procesados (aceptados) hasta el momento.
    # la llamada que invoca esta función debe incrementarlos de forma
    # consistente (ver dashboard.py). El filtro descarta ARP adicionales
    # cuando la proporción excede el límite configurado.
    current_ratio = arp_count / max(packets_count, 1)
    return current_ratio <= arp_ratio


def filter_arp_dataframe(df, arp_limit_mode='low'):
    """
    Filtra paquetes ARP del DataFrame según el modo especificado.
    Usa muestreo aleatorio para mantener representatividad.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los paquetes capturados (debe tener columna 'protocols')
    arp_limit_mode : str
        Modo de límite de ARP: 'low', 'medium', 'high', 'none'
    
    Returns:
    --------
    pd.DataFrame
        DataFrame filtrado con reducción de paquetes ARP según el modo
    """
    if df is None or df.empty or 'protocols' not in df.columns:
        return df
    
    if arp_limit_mode == 'none':
        return df
    
    # Determinar porcentaje de ARP a mantener
    # para el filtrado posterior a la captura usamos los mismos valores
    # aproximados; note que la función actual no se utiliza en todo el
    # flujo, pero se conserva para procesar CSVs o capturas manuales.
    retention_rates = {
        'low': 0.15,
        'medium': 0.30,
        'high': 0.50
    }
    
    retention_rate = retention_rates.get(arp_limit_mode, 0.15)
    
    # Separar ARP y no-ARP
    arp_mask = df['protocols'] == 'ARP'
    non_arp_df = df[~arp_mask]
    arp_df = df[arp_mask]
    
    # Si no hay ARP, retornar original
    if arp_df.empty:
        return df
    
    # Muestrear ARP según el porcentaje
    num_arp_to_keep = max(1, int(len(arp_df) * retention_rate))
    arp_df_filtered = arp_df.sample(n=num_arp_to_keep, random_state=42)
    
    # Combinar y reordenar
    result_df = pd.concat([non_arp_df, arp_df_filtered], ignore_index=False)
    result_df = result_df.sort_index().reset_index(drop=True)
    
    return result_df


def get_arp_filter_description(arp_limit_mode):
    """
    Retorna una descripción legible del modo de filtro ARP.
    
    Parameters:
    -----------
    arp_limit_mode : str
        Modo de límite de ARP
    
    Returns:
    --------
    str
        Descripción amigable del modo
    """
    descriptions = {
        'low': '🟢 Bajo (≈15% ARP) - Recomendado para mejor precisión',
        'medium': '🟡 Medio (≈30% ARP) - Balance entre ARP y otros paquetes',
        'high': '🔴 Alto (≈50% ARP) - Más ARP pero sigue filtrando',
        'none': '⚪ Sin filtro (todos los paquetes) - Captura completa'
    }
    
    return descriptions.get(arp_limit_mode, 'Modo desconocido')
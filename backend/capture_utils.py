import glob
import shlex
import os
import signal
import tempfile
import subprocess
from subprocess import PIPE, DEVNULL, Popen
import pandas as pd


# Columnas (en orden) que genera type_packet para cada paquete capturado.
CAPTURE_FIELDNAMES = [
    'delta_time', 'protocols','ip_src','ip_dst','port_src', 'port_dst', 'frame_len',
    'udp_len', 'ip_ttl', 'icmp_type', 'tos', 'ip_flags_rb', 'ip_flags_df', 'ip_flags_mf',
    'tcp_flags_res', 'tcp_flags_ns', 'tcp_flags_cwr', 'tcp_flags_ecn', 'tcp_flags_urg',
    'tcp_flags_ack', 'tcp_flags_push', 'tcp_flags_reset', 'tcp_flags_syn', 'tcp_flags_fin','epoch_time'
]

CAPTURE_NUMERIC_COLUMNS = {
    'delta_time',
    'port_src',
    'port_dst',
    'frame_len',
    'udp_len',
    'ip_ttl',
    'icmp_type',
    'tos',
    'ip_flags_rb',
    'ip_flags_df',
    'ip_flags_mf',
    'tcp_flags_res',
    'tcp_flags_ns',
    'tcp_flags_cwr',
    'tcp_flags_ecn',
    'tcp_flags_urg',
    'tcp_flags_ack',
    'tcp_flags_push',
    'tcp_flags_reset',
    'tcp_flags_syn',
    'tcp_flags_fin',
    'epoch_time',
}


def _normalize_dataframe_types(df):
    """Normaliza tipos para evitar columnas mixtas al serializar o predecir."""
    if df is None or df.empty:
        return df

    normalized = df.copy()

    for column in CAPTURE_NUMERIC_COLUMNS.intersection(normalized.columns):
        normalized[column] = pd.to_numeric(
            normalized[column].astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0)

    for column in ('protocols', 'ip_src', 'ip_dst'):
        if column in normalized.columns:
            normalized[column] = normalized[column].astype('string').fillna('')

    return normalized


def _detect_active_interface():
    """Detecta la interfaz de red activa (con estado UP y carrier)."""
    try:
        result = subprocess.run(
            ['ip', '-o', 'link', 'show'],
            capture_output=True, text=True, timeout=5
        )
        # Prioridad: wlan0 > eth0 > cualquier otra
        for iface_name in ['wlan0', 'eth0']:
            for line in result.stdout.strip().split('\n'):
                if iface_name in line and 'state UP' in line:
                    return iface_name
        # Fallback: primera interfaz UP que no sea lo/docker/tailscale
        for line in result.stdout.strip().split('\n'):
            if 'state UP' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    name = parts[1].strip()
                    if name not in ('lo', 'docker0', 'tailscale0'):
                        return name
    except Exception:
        pass
    return 'wlan0'  # Default


def build_tshark_command() -> list:
    iface = _detect_active_interface()
    comm_arg = (
        f"tshark "
        f"-i {iface} "
        "-l "
        "-f \"tcp or udp or arp or icmp\" "
        "-T fields -E separator=/t "
        "-e frame.time_delta "
        "-e _ws.col.Protocol "
        "-e ip.src -e ip.dst "
        "-e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 "
        "-e ipv6.src -e ipv6.dst "
        "-e eth.src -e eth.dst "
        "-e tcp.srcport -e tcp.dstport "
        "-e udp.srcport -e udp.dstport "
        "-e frame.len -e udp.length "
        "-e ip.ttl -e icmp.type "
        "-e ip.dsfield.dscp -e ip.flags.rb -e ip.flags.df -e ip.flags.mf "
        "-e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn "
        "-e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset "
        "-e tcp.flags.syn -e tcp.flags.fin -e ip.version "
        "-e frame.time_epoch"
    )
    return shlex.split(comm_arg)


def capturing_packets(comm_arg):
    process = Popen(
        comm_arg,
        stdout=PIPE,
        stderr=DEVNULL,
        text=True,
        bufsize=1,
        start_new_session=True,
    )
    return process


def stop_capture_process(process, timeout=5):
    if process is None:
        return

    stdout = getattr(process, 'stdout', None)
    stderr = getattr(process, 'stderr', None)

    try:
        if process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except Exception:
                    pass
                try:
                    process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except Exception:
                        pass
                    try:
                        process.kill()
                    except Exception:
                        pass
                    try:
                        process.wait(timeout=timeout)
                    except Exception:
                        pass
            except Exception:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except Exception:
                    pass
                try:
                    process.kill()
                except Exception:
                    pass
                try:
                    process.wait(timeout=timeout)
                except Exception:
                    pass
    finally:
        for stream in (stdout, stderr):
            try:
                if stream is not None:
                    stream.close()
            except Exception:
                pass

        temp_dir = tempfile.gettempdir()
        for temp_path in glob.glob(os.path.join(temp_dir, 'wireshark_*.pcapng*')):
            try:
                os.remove(temp_path)
            except Exception:
                pass


def type_packet(packet_):
    if len(packet_) < 34:  # Rellenar con valores vacíos si falta información
        packet_ += [''] * (34 - len(packet_))

    if packet_[1] in ['TCP', 'SSH', 'SSHv2', 'TLSv1.2', 'HTTP']:
        tcp_src = packet_[10]
        tcp_dst = packet_[11]
    elif packet_[1] in ['UDP', 'DNS', 'BROWSER', 'DHCP']:
        tcp_src = packet_[12]
        tcp_dst = packet_[13]
    else:
        tcp_src = ''
        tcp_dst = ''

    if packet_[1] == 'ARP':
        packet_[2] = packet_[4]  # ip.src <- arp.src.proto_ipv4
        packet_[3] = packet_[5]  # ip.dst <- arp.dst.proto_ipv4

    if packet_[32] == '6':
        packet_[2] = packet_[6]  # ip.src <- ipv6.src
        packet_[3] = packet_[7]  # ip.dst <- ipv6.dst

    for index in [16, 18, 19, 20, 21]:
        if packet_[index]:
            packet_[index] = packet_[index].replace(',', '.')

    ordered_packet = [
        packet_[0], packet_[1], packet_[2], packet_[3], tcp_src, tcp_dst, packet_[14], packet_[15],
        packet_[16], packet_[17], packet_[18], packet_[19], packet_[20], packet_[21], packet_[22],
        packet_[23], packet_[24], packet_[25], packet_[26], packet_[27], packet_[28], packet_[29],
        packet_[30], packet_[31], packet_[33]
    ]

    return {CAPTURE_FIELDNAMES[i]: ordered_packet[i] for i in range(len(CAPTURE_FIELDNAMES))}


def packet_df(type_packet_dict, df):
    df_temp = pd.DataFrame(type_packet_dict)
    if list(df_temp.columns) == ['value']:
        return df  # Ignorar tablas value
    if df is None:
        df = df_temp
    else:
        df = pd.concat([df, df_temp], axis=0, ignore_index=True)
    if list(df.columns) == ['value']:
        return None
    return df

def build_dataframe_from_rows(rows):
    """Construye el DataFrame una sola vez a partir de una lista de dicts.
    Reemplaza la concatenación paquete a paquete (O(n^2)) por una sola
    construcción O(n) al final de la captura."""
    if not rows:
        return None
    return pd.DataFrame(rows)

def apply_arp_filter(df, arp_limit_mode='low'):
    """
    Filtra paquetes ARP del DataFrame según el modo especificado.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los paquetes capturados
    arp_limit_mode : str
        Modo de límite de ARP: 'low' (por defecto), 'medium', 'high', 'none'
        - 'low': Mantiene solo el 20% de paquetes ARP
        - 'medium': Mantiene el 50% de paquetes ARP
        - 'high': Mantiene el 80% de paquetes ARP
        - 'none': No filtra ARP (mantiene todos)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame filtrado con reducción de paquetes ARP
    """
    if df is None or df.empty or 'protocols' not in df.columns:
        return df
    
    if arp_limit_mode == 'none':
        return df
    
    # Identificar paquetes ARP y no-ARP
    arp_mask = df['protocols'] == 'ARP'
    non_arp_df = df[~arp_mask]
    arp_df = df[arp_mask]
    
    # Si no hay paquetes ARP, retornar el DataFrame original
    if arp_df.empty:
        return df
    
    # Determinar qué porcentaje de paquetes ARP mantener
    retention_rate = {
        'low': 0.20,      # Mantiene 20% de ARP
        'medium': 0.50,   # Mantiene 50% de ARP
        'high': 0.80      # Mantiene 80% de ARP
    }.get(arp_limit_mode, 0.20)
    
    # Muestrear paquetes ARP según el porcentaje
    num_arp_to_keep = max(1, int(len(arp_df) * retention_rate))
    arp_df_filtered = arp_df.sample(n=num_arp_to_keep, random_state=42)
    
    # Combinar y reordenar por índice original
    result_df = pd.concat([non_arp_df, arp_df_filtered], ignore_index=False)
    result_df = result_df.sort_index().reset_index(drop=True)
    
    return result_df
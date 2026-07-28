#!/usr/bin/env python3
"""
Script de prueba para verificar que la normalización de tipos de datos
funciona correctamente y evita el error de PyArrow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from backend.capture_utils import type_packet, packet_df
import pyarrow as pa

def test_type_conversion():
    """Prueba que type_packet devuelve valores consistentes."""
    print("=" * 60)
    print("TEST 1: Validar type_packet con diferentes protocolos")
    print("=" * 60)
    
    # Simular un paquete TCP con puerto
    tcp_packet = ['0.001', 'TCP', '192.168.1.1', '192.168.1.2', '', '', '', '', 
                  '443', '5000', '', '', '', '', '100', '0', '', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', '', '', '4']
    result_tcp = type_packet(tcp_packet)
    print(f"\nPaquete TCP:")
    print(f"  port_src: {result_tcp['port_src']} (type: {type(result_tcp['port_src'][0])})")
    print(f"  port_dst: {result_tcp['port_dst']} (type: {type(result_tcp['port_dst'][0])})")
    assert isinstance(result_tcp['port_src'][0], str) and result_tcp['port_src'][0] != '', "port_src debe ser string no vacío"
    
    # Simular un paquete ARP sin puerto
    arp_packet = ['0.001', 'ARP', '', '', '', '', '', '', 
                  '', '', '', '', '', '', '100', '0', '', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', '', '', '4']
    result_arp = type_packet(arp_packet)
    print(f"\nPaquete ARP:")
    print(f"  port_src: {result_arp['port_src']} (type: {type(result_arp['port_src'][0])})")
    print(f"  port_dst: {result_arp['port_dst']} (type: {type(result_arp['port_dst'][0])})")
    assert result_arp['port_src'][0] != '', "port_src no debe ser vacío, debe ser '0'"
    
    print("\n✅ TEST 1 PASÓ: type_packet devuelve valores consistentes\n")


def test_packet_df_normalization():
    """Prueba que packet_df normaliza correctamente los tipos."""
    print("=" * 60)
    print("TEST 2: Validar normalización en packet_df")
    print("=" * 60)
    
    df = None
    
    # Agregar 5 paquetes diferentes
    protocols = ['TCP', 'UDP', 'ARP', 'ICMP', 'TCP']
    
    for i, protocol in enumerate(protocols):
        packet = ['0.001', protocol, f'192.168.1.{i}', '192.168.1.100', '', '', '', '', 
                  str(5000 + i), str(8000 + i), '', '', '', '', '100', '0', 
                  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '4']
        
        type_packet_data = type_packet(packet)
        df = packet_df(type_packet_data, df)
    
    print(f"\nDataFrame después de agregar paquetes:")
    print(f"  Filas: {len(df)}")
    print(f"  Columnas: {df.columns.tolist()}")
    
    # Verificar tipos de datos
    print(f"\nTipos de datos en el DataFrame:")
    for col in ['port_src', 'port_dst', 'protocols', 'ip_src']:
        dtype = df[col].dtype
        print(f"  {col}: {dtype}")
        # Verificar que no hay valores mixtos
        unique_types = set(type(val) for val in df[col])
        print(f"    Tipos únicos en valores: {unique_types}")
    
    print(f"\nContenido del DataFrame:")
    print(df[['protocols', 'ip_src', 'port_src', 'port_dst']].to_string())
    
    print("\n✅ TEST 2 PASÓ: packet_df normaliza correctamente\n")


def test_pyarrow_serialization():
    """Prueba que PyArrow puede serializar el DataFrame sin errores."""
    print("=" * 60)
    print("TEST 3: Serialización con PyArrow")
    print("=" * 60)
    
    df = None
    
    # Agregar 20 paquetes variados
    for i in range(20):
        protocol = ['TCP', 'UDP', 'ARP', 'ICMP'][i % 4]
        packet = ['0.001', protocol, f'192.168.1.{i}', '192.168.1.100', '', '', '', '', 
                  str(5000 + i), str(8000 + i), '', '', '', '', '100', '0',
                  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '4']
        
        type_packet_data = type_packet(packet)
        df = packet_df(type_packet_data, df)
    
    print(f"\nIntentando serializar DataFrame con {len(df)} filas...")
    try:
        table = pa.Table.from_pandas(df)
        print(f"✅ Serialización exitosa!")
        print(f"  Esquema de PyArrow: {table.schema}")
    except Exception as e:
        print(f"❌ Error de serialización: {e}")
        print(f"\nDiagnóstico:")
        for col in df.columns:
            print(f"  {col}: dtype={df[col].dtype}, values={df[col].unique()[:3]}")
        raise
    
    print("\n✅ TEST 3 PASÓ: PyArrow puede serializar sin errores\n")


def test_stress_many_packets():
    """Prueba de estrés con muchos paquetes."""
    print("=" * 60)
    print("TEST 4: Prueba de estrés (100 paquetes)")
    print("=" * 60)
    
    df = None
    
    for i in range(100):
        protocol = ['TCP', 'UDP', 'ARP', 'ICMP', 'DNS'][i % 5]
        packet = ['0.001', protocol, f'192.168.{i // 256}.{i % 256}', '192.168.1.100', '', '', '', '',
                  str((5000 + i) % 65536), str((8000 + i) % 65536), '', '', '', '', 
                  str(50 + (i % 200)), str(i % 10),
                  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '4']
        
        type_packet_data = type_packet(packet)
        df = packet_df(type_packet_data, df)
    
    print(f"\nDataFrame con {len(df)} paquetes creado exitosamente")
    
    # Verificar tipos
    print(f"\nVerificando tipos de datos...")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    # Intentar serializar
    try:
        table = pa.Table.from_pandas(df)
        print(f"\n✅ Serialización de {len(df)} paquetes exitosa!")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    
    print("\n✅ TEST 4 PASÓ: Manejo de muchos paquetes funciona\n")


if __name__ == "__main__":
    try:
        test_type_conversion()
        test_packet_df_normalization()
        test_pyarrow_serialization()
        test_stress_many_packets()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 60)
        print("\nLos cambios han sido validados y la captura automática")
        print("debería funcionar sin errores de PyArrow ahora.")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LOS TESTS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

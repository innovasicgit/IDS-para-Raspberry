#!/usr/bin/env python3
"""
Test rápido del Backend API
Verifica que todos los endpoints funcionen correctamente
"""

import requests
import json
import time
from typing import Dict, Any

# Configuración
BACKEND_URL = "http://localhost:8000"
TIMEOUT = 10

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def test_endpoint(name: str, method: str, endpoint: str, payload: Dict[str, Any] = None) -> bool:
    """Prueba un endpoint y reporta el resultado"""
    print(f"\n{'='*60}")
    print(f"🧪 Test: {name}")
    print(f"{'='*60}")
    
    try:
        url = f"{BACKEND_URL}{endpoint}"
        print(f"📡 {method} {url}")
        
        start = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=TIMEOUT)
        else:
            raise ValueError(f"Método no soportado: {method}")
        
        elapsed = time.time() - start
        
        print(f"⏱️  Tiempo: {elapsed:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            print(f"{GREEN}✅ PASS{RESET}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            print(f"{RED}❌ FAIL{RESET}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"{RED}❌ FAIL: No se puede conectar al backend{RESET}")
        print("Asegúrate de que el backend esté corriendo:")
        print("  python backend_api.py")
        return False
    except requests.exceptions.Timeout:
        print(f"{RED}❌ FAIL: Timeout{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ FAIL: {str(e)}{RESET}")
        return False


def main():
    print(f"""
    {'='*60}
    🧪 TEST SUITE - Backend API
    {'='*60}
    Backend URL: {BACKEND_URL}
    """)
    
    # Verificar que el backend esté corriendo
    print("\n🔍 Verificando que el backend esté disponible...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}✅ Backend disponible{RESET}\n")
        else:
            print(f"{RED}❌ Backend no responde correctamente{RESET}")
            return
    except:
        print(f"{RED}❌ Backend no disponible{RESET}")
        print(f"\n{YELLOW}Inicia el backend con:{RESET}")
        print("  python backend_api.py")
        print("\no:")
        print("  ./start_backend.sh")
        return
    
    # Ejecutar tests
    results = []
    
    # Test 1: Root endpoint
    results.append(test_endpoint(
        "Root Health Check",
        "GET",
        "/"
    ))
    
    # Test 2: Health endpoint
    results.append(test_endpoint(
        "Detailed Health Check",
        "GET",
        "/health"
    ))
    
    # Test 3: System metrics
    results.append(test_endpoint(
        "System Metrics",
        "GET",
        "/metrics"
    ))
    
    # Test 4: Models list
    results.append(test_endpoint(
        "Available Models",
        "GET",
        "/models"
    ))
    
    # Test 5: Captura corta (requiere tshark y permisos)
    print(f"\n{YELLOW}⚠️  El siguiente test requiere tshark configurado y permisos{RESET}")
    print("Si falla, es normal si no tienes wireshark configurado")
    time.sleep(2)
    
    results.append(test_endpoint(
        "Short Packet Capture (10s)",
        "POST",
        "/capture",
        payload={
            "duration": 10,
            "arp_filter_mode": "low"
        }
    ))
    
    # Resumen
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE TESTS")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTotal: {total}")
    print(f"{GREEN}Exitosos: {passed}{RESET}")
    print(f"{RED}Fallidos: {total - passed}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 ¡Todos los tests pasaron!{RESET}")
        print(f"\n{GREEN}✅ El backend está funcionando correctamente{RESET}")
    elif passed >= total - 1:
        print(f"\n{YELLOW}⚠️  Casi perfecto (probablemente falta configurar tshark){RESET}")
        print("\nPara habilitar captura de paquetes:")
        print("  sudo apt install tshark")
        print("  sudo usermod -a -G wireshark $USER")
    else:
        print(f"\n{RED}❌ Varios tests fallaron{RESET}")
        print("\nVerifica:")
        print("  1. Backend está corriendo")
        print("  2. Modelos ML están en la carpeta 'model/'")
        print("  3. Dependencias instaladas (requirements_backend.txt)")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()

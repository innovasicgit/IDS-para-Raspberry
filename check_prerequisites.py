#!/usr/bin/env python3
"""
Verificador de prerequisitos para el Backend API
Ejecutar antes de start_backend.sh para verificar que todo esté configurado
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

# Colores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def check_python_version():
    """Verifica versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    if version >= (3, 9):
        print(f"{GREEN}✅ Python {version.major}.{version.minor}.{version.micro}{RESET}")
        return True
    else:
        print(f"{RED}❌ Python 3.9+ requerido, tienes {version.major}.{version.minor}{RESET}")
        return False

def check_tshark():
    """Verifica instalación de tshark"""
    print("\n📡 Verificando tshark...")
    
    tshark_path = shutil.which('tshark')
    if tshark_path:
        print(f"{GREEN}✅ tshark encontrado: {tshark_path}{RESET}")
        
        # Verificar permisos
        try:
            result = subprocess.run(
                ['groups'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'wireshark' in result.stdout:
                print(f"{GREEN}✅ Usuario en grupo 'wireshark'{RESET}")
                return True
            else:
                print(f"{YELLOW}⚠️  Usuario NO está en grupo 'wireshark'{RESET}")
                print(f"{YELLOW}   Ejecuta: sudo usermod -a -G wireshark $USER{RESET}")
                print(f"{YELLOW}   Luego cierra sesión y vuelve a entrar{RESET}")
                return False
        except:
            print(f"{YELLOW}⚠️  No se pudo verificar grupo 'wireshark'{RESET}")
            return False
    else:
        print(f"{RED}❌ tshark no encontrado{RESET}")
        print(f"{YELLOW}   Instala con: sudo apt install tshark{RESET}")
        return False

def check_models():
    """Verifica que existan los modelos ML"""
    print("\n🤖 Verificando modelos ML...")
    
    model_dir = Path("model")
    required_models = [
        "iforest__EJERCICIO10_n_components6_fit.pkl",
        "ocsvm__EJERCICIO10_n_components6_fit.pkl",
        "kmeans1__EJERCICIO10_n_components6_over.pkl",
        "autoencoder.pkl",
        "list_kmeans_over.txt"
    ]
    
    if not model_dir.exists():
        print(f"{RED}❌ Carpeta 'model/' no encontrada{RESET}")
        return False
    
    all_ok = True
    for model_file in required_models:
        model_path = model_dir / model_file
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"{GREEN}✅ {model_file} ({size_mb:.1f} MB){RESET}")
        else:
            print(f"{RED}❌ {model_file} no encontrado{RESET}")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias Python...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas',
        'numpy',
        'sklearn',
        'joblib',
        'psutil',
        'pyod'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"{GREEN}✅ {package}{RESET}")
        except ImportError:
            print(f"{RED}❌ {package} no instalado{RESET}")
            missing.append(package)
    
    if missing:
        print(f"\n{YELLOW}Instala las dependencias faltantes con:{RESET}")
        print(f"  pip install -r requirements_backend.txt")
        return False
    
    return True

def check_files():
    """Verifica que existan los archivos necesarios"""
    print("\n📄 Verificando archivos del proyecto...")
    
    required_files = [
        "backend_api.py",
        "requirements_backend.txt",
        "backend/capture_utils.py",
        "backend/predict.py",
        "backend/model_utils.py",
        "backend/constants.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"{GREEN}✅ {file_path}{RESET}")
        else:
            print(f"{RED}❌ {file_path} no encontrado{RESET}")
            all_ok = False
    
    return all_ok

def check_network():
    """Muestra información de red"""
    print("\n🌐 Información de red...")
    
    try:
        result = subprocess.run(
            ['hostname', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )
        ips = result.stdout.strip().split()
        if ips:
            print(f"{GREEN}✅ IPs disponibles:{RESET}")
            for ip in ips:
                print(f"   • {ip}")
        else:
            print(f"{YELLOW}⚠️  No se encontraron IPs{RESET}")
    except:
        print(f"{YELLOW}⚠️  No se pudo obtener información de red{RESET}")
    
    return True

def check_port():
    """Verifica si el puerto 8000 está disponible"""
    print("\n🔌 Verificando puerto 8000...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print(f"{YELLOW}⚠️  Puerto 8000 ya está en uso{RESET}")
            print(f"{YELLOW}   Puede que el backend ya esté corriendo{RESET}")
            print(f"{YELLOW}   O verifica con: sudo lsof -i:8000{RESET}")
            return False
        else:
            print(f"{GREEN}✅ Puerto 8000 disponible{RESET}")
            return True
    except:
        print(f"{YELLOW}⚠️  No se pudo verificar puerto{RESET}")
        return True

def main():
    print_header("🔍 VERIFICADOR DE PREREQUISITOS")
    print("Verificando que el sistema esté listo para el Backend API...\n")
    
    checks = {
        "Python 3.9+": check_python_version(),
        "tshark y permisos": check_tshark(),
        "Modelos ML": check_models(),
        "Dependencias Python": check_dependencies(),
        "Archivos del proyecto": check_files(),
        "Información de red": check_network(),
        "Puerto 8000 disponible": check_port()
    }
    
    # Resumen
    print_header("📊 RESUMEN")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"{check_name:.<40} {status}")
    
    print(f"\n{'-'*60}")
    print(f"Total: {passed}/{total} checks pasados")
    print(f"{'-'*60}\n")
    
    if passed == total:
        print(f"{GREEN}🎉 ¡Sistema listo!{RESET}")
        print(f"\n{GREEN}Puedes iniciar el backend con:{RESET}")
        print(f"  ./start_backend.sh")
        print(f"\n{GREEN}O manualmente:{RESET}")
        print(f"  python backend_api.py")
    elif passed >= total - 1:
        print(f"{YELLOW}⚠️  Casi listo (revisa los warnings arriba){RESET}")
        print(f"\nPuedes intentar iniciar el backend, pero puede que algunas")
        print(f"funcionalidades no estén disponibles.")
    else:
        print(f"{RED}❌ Sistema NO está listo{RESET}")
        print(f"\nPor favor, resuelve los problemas indicados arriba antes de continuar.")
        print(f"\nConsulta la documentación:")
        print(f"  • INICIO_RAPIDO.md")
        print(f"  • ARQUITECTURA_API.md")
    
    print(f"\n{'-'*60}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

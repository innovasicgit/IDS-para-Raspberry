#!/usr/bin/env python3
"""
Generador de Informe de Estado del Sistema
Crea un reporte completo del estado del Backend API
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path

def run_command(cmd):
    """Ejecuta comando y retorna output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except:
        return "N/A"

def get_file_info(path):
    """Obtiene info de un archivo"""
    try:
        p = Path(path)
        if p.exists():
            size = p.stat().st_size
            modified = datetime.fromtimestamp(p.stat().st_mtime)
            return {
                "exists": True,
                "size": size,
                "size_mb": size / (1024 * 1024),
                "modified": modified.strftime("%Y-%m-%d %H:%M:%S")
            }
        return {"exists": False}
    except:
        return {"exists": False, "error": True}

def check_backend_running():
    """Verifica si el backend está corriendo"""
    result = run_command("ps aux | grep '[b]ackend_api.py'")
    return bool(result)

def get_backend_pid():
    """Obtiene PID del backend"""
    result = run_command("ps aux | grep '[b]ackend_api.py' | awk '{print $2}'")
    return result if result else "N/A"

def generate_report():
    """Genera reporte completo"""
    
    report = []
    report.append("=" * 70)
    report.append("📊 INFORME DE ESTADO DEL SISTEMA - IDS IoT Backend API")
    report.append("=" * 70)
    report.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Usuario: {os.getenv('USER', 'unknown')}")
    report.append(f"Hostname: {run_command('hostname')}")
    report.append("")
    
    # Sistema
    report.append("-" * 70)
    report.append("🖥️  INFORMACIÓN DEL SISTEMA")
    report.append("-" * 70)
    report.append(f"SO: {run_command('uname -s')}")
    report.append(f"Arquitectura: {run_command('uname -m')}")
    report.append(f"Kernel: {run_command('uname -r')}")
    report.append(f"Uptime: {run_command('uptime -p')}")
    report.append("")
    
    # Python
    report.append("-" * 70)
    report.append("🐍 ENTORNO PYTHON")
    report.append("-" * 70)
    report.append(f"Python: {run_command('python3 --version')}")
    report.append(f"Pip: {run_command('pip --version')}")
    
    # Verificar paquetes clave
    packages = ['fastapi', 'uvicorn', 'pandas', 'sklearn']
    for pkg in packages:
        version = run_command(f"pip show {pkg} 2>/dev/null | grep Version | cut -d' ' -f2")
        status = "✅" if version else "❌"
        report.append(f"{status} {pkg}: {version if version else 'No instalado'}")
    report.append("")
    
    # Backend
    report.append("-" * 70)
    report.append("🚀 ESTADO DEL BACKEND")
    report.append("-" * 70)
    
    is_running = check_backend_running()
    report.append(f"Estado: {'✅ CORRIENDO' if is_running else '❌ DETENIDO'}")
    
    if is_running:
        pid = get_backend_pid()
        report.append(f"PID: {pid}")
        
        # Recursos del proceso
        cpu = run_command(f"ps -p {pid} -o %cpu | tail -1")
        mem = run_command(f"ps -p {pid} -o %mem | tail -1")
        report.append(f"CPU: {cpu}%")
        report.append(f"Memoria: {mem}%")
        
        # Puerto
        port_check = run_command("lsof -i:8000 2>/dev/null | grep LISTEN")
        report.append(f"Puerto 8000: {'✅ Activo' if port_check else '⚠️ No detectado'}")
    
    report.append("")
    
    # Archivos del proyecto
    report.append("-" * 70)
    report.append("📁 ARCHIVOS DEL PROYECTO")
    report.append("-" * 70)
    
    key_files = [
        "backend_api.py",
        "app_cloud.py",
        "requirements_backend.txt",
        "requirements_frontend.txt",
        "start_backend.sh",
        "stop_backend.sh"
    ]
    
    for file in key_files:
        info = get_file_info(file)
        if info['exists']:
            report.append(f"✅ {file} ({info['size_mb']:.2f} MB) - {info['modified']}")
        else:
            report.append(f"❌ {file} - No encontrado")
    
    report.append("")
    
    # Modelos ML
    report.append("-" * 70)
    report.append("🤖 MODELOS ML")
    report.append("-" * 70)
    
    models = [
        "model/iforest__EJERCICIO10_n_components6_fit.pkl",
        "model/ocsvm__EJERCICIO10_n_components6_fit.pkl",
        "model/kmeans1__EJERCICIO10_n_components6_over.pkl",
        "model/autoencoder.pkl"
    ]
    
    total_size = 0
    for model in models:
        info = get_file_info(model)
        if info['exists']:
            total_size += info['size_mb']
            report.append(f"✅ {Path(model).name} ({info['size_mb']:.1f} MB)")
        else:
            report.append(f"❌ {Path(model).name} - No encontrado")
    
    report.append(f"\nTamaño total modelos: {total_size:.1f} MB")
    report.append("")
    
    # Red
    report.append("-" * 70)
    report.append("🌐 CONFIGURACIÓN DE RED")
    report.append("-" * 70)
    
    ips = run_command("hostname -I").split()
    if ips:
        report.append("IPs disponibles:")
        for ip in ips:
            report.append(f"  • {ip}")
    
    # Interfaces
    interfaces = run_command("ls /sys/class/net/").split()
    if interfaces:
        report.append("\nInterfaces de red:")
        for iface in interfaces:
            status = run_command(f"cat /sys/class/net/{iface}/operstate 2>/dev/null")
            report.append(f"  • {iface}: {status if status else 'unknown'}")
    
    report.append("")
    
    # Recursos del sistema
    report.append("-" * 70)
    report.append("💻 RECURSOS DEL SISTEMA")
    report.append("-" * 70)
    
    # CPU
    cpu_usage = run_command("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'")
    report.append(f"CPU: {cpu_usage}%")
    
    # Memoria
    mem_info = run_command("free -m | grep Mem | awk '{print $3,$2}'")
    if mem_info:
        used, total = mem_info.split()
        percent = (int(used) / int(total)) * 100
        report.append(f"Memoria: {used}/{total} MB ({percent:.1f}%)")
    
    # Disco
    disk_info = run_command("df -h / | tail -1 | awk '{print $3,$2,$5}'")
    if disk_info:
        used, total, percent = disk_info.split()
        report.append(f"Disco: {used}/{total} ({percent})")
    
    report.append("")
    
    # Logs
    report.append("-" * 70)
    report.append("📝 LOGS RECIENTES")
    report.append("-" * 70)
    
    if Path("backend.log").exists():
        report.append("Últimas 10 líneas de backend.log:")
        last_lines = run_command("tail -10 backend.log")
        for line in last_lines.split('\n'):
            report.append(f"  {line}")
    else:
        report.append("❌ backend.log no encontrado")
    
    report.append("")
    
    # Recomendaciones
    report.append("-" * 70)
    report.append("💡 RECOMENDACIONES")
    report.append("-" * 70)
    
    recommendations = []
    
    if not is_running:
        recommendations.append("⚠️  Backend no está corriendo. Ejecuta: ./start_backend.sh")
    
    if not run_command("groups | grep wireshark"):
        recommendations.append("⚠️  Usuario no en grupo 'wireshark'. Ejecuta: sudo usermod -a -G wireshark $USER")
    
    if float(cpu_usage.replace('%', '')) > 80 if cpu_usage else False:
        recommendations.append("⚠️  CPU alta (>80%). Considera optimizar o reducir duración de capturas")
    
    if not recommendations:
        recommendations.append("✅ Sistema en buen estado. No hay recomendaciones.")
    
    for rec in recommendations:
        report.append(rec)
    
    report.append("")
    report.append("=" * 70)
    report.append("Fin del informe")
    report.append("=" * 70)
    
    return '\n'.join(report)

def main():
    print("\n🔍 Generando informe de estado del sistema...\n")
    
    report = generate_report()
    
    # Imprimir en consola
    print(report)
    
    # Guardar a archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"system_report_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n💾 Informe guardado en: {filename}")
    except Exception as e:
        print(f"\n⚠️  No se pudo guardar el informe: {e}")
    
    print()

if __name__ == "__main__":
    main()

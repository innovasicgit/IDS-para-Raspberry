# 🏗️ Arquitectura API Backend + Frontend Cloud

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura](#arquitectura)
3. [Instalación Backend (Raspberry Pi)](#instalación-backend)
4. [Instalación Frontend (Streamlit Cloud)](#instalación-frontend)
5. [Configuración de Red](#configuración-de-red)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Descripción General

Esta arquitectura separa el **backend pesado** (captura de red + modelos ML) que corre en la Raspberry Pi, del **frontend ligero** (interfaz visual) que corre en Streamlit Cloud.

### Ventajas
✅ **Frontend fluido**: Animaciones y UI sin lag en Streamlit Cloud  
✅ **Backend optimizado**: Solo API REST ligera en la Raspberry  
✅ **Escalable**: Puedes conectar múltiples frontends al mismo backend  
✅ **Seguro**: Datos sensibles nunca salen de tu red local  

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│   Streamlit Cloud (Frontend)            │
│   - app_cloud.py                        │
│   - UI/UX dinámico                      │
│   - Gráficos con Plotly                 │
└────────────┬────────────────────────────┘
             │ HTTP/HTTPS
             │ requests.post()
             ▼
┌─────────────────────────────────────────┐
│   Raspberry Pi (Backend API)            │
│   - FastAPI (backend_api.py)            │
│   - Captura de paquetes (tshark)        │
│   - Modelos ML (IForest, OCSVM, etc.)   │
│   - Procesamiento de datos              │
└────────────┬────────────────────────────┘
             │
             ▼
      [Interfaces de Red]
      eth0, wlan0, etc.
```

---

## 🔧 Instalación Backend (Raspberry Pi)

### 1. Instalar dependencias del sistema

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar tshark
sudo apt install -y tshark wireshark

# Dar permisos a tshark
sudo dpkg-reconfigure wireshark-common  # Seleccionar "Yes"
sudo usermod -a -G wireshark $USER
newgrp wireshark
```

### 2. Crear entorno virtual

```bash
cd "~/Desktop/IDS para raspberry v2"

# Si no existe el entorno
python3 -m venv backend_env
source backend_env/bin/activate
```

### 3. Instalar dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements_backend.txt
```

### 4. Verificar que los modelos existen

```bash
ls -lh model/
# Deberías ver:
# - iforest__EJERCICIO10_n_components6_fit.pkl
# - ocsvm__EJERCICIO10_n_components6_fit.pkl
# - kmeans1__EJERCICIO10_n_components6_over.pkl
# - autoencoder.pkl
# - list_kmeans_over.txt
```

### 5. Ejecutar el backend

```bash
# Activar entorno si no está activado
source backend_env/bin/activate

# Ejecutar API
python backend_api.py
```

Deberías ver:
```
🚀 Iniciando Backend API para IDS IoT...
🔄 Cargando modelos ML...
✅ Modelos cargados correctamente
✅ Servidor listo para recibir peticiones
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. (Opcional) Ejecutar como servicio systemd

Crea `/etc/systemd/system/ids-backend.service`:

```ini
[Unit]
Description=IDS IoT Backend API
After=network.target

[Service]
Type=simple
User=innovasic
WorkingDirectory=/home/innovasic/Desktop/IDS para raspberry v2
Environment="PATH=/home/innovasic/Desktop/IDS para raspberry v2/backend_env/bin"
ExecStart=/home/innovasic/Desktop/IDS para raspberry v2/backend_env/bin/python backend_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Luego:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ids-backend
sudo systemctl start ids-backend
sudo systemctl status ids-backend
```

---

## ☁️ Instalación Frontend (Streamlit Cloud)

### 1. Preparar repositorio

```bash
# Crear carpeta separada para el frontend (opcional)
mkdir ids-frontend
cd ids-frontend

# Copiar solo lo necesario
cp ../app_cloud.py app.py
cp ../requirements_frontend.txt requirements.txt
cp ../.env.example .env

# Editar .env con la URL de tu Raspberry
nano .env
# Cambiar: BACKEND_API_URL=http://TU_IP_RASPBERRY:8000
```

### 2. Subir a GitHub

```bash
git init
git add .
git commit -m "Frontend IDS IoT"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ids-frontend.git
git push -u origin main
```

### 3. Deploy en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio `ids-frontend`
3. Configura:
   - **Main file**: `app.py`
   - **Python version**: 3.11
4. En **Advanced settings** → **Secrets**, añade:
   ```toml
   BACKEND_API_URL = "http://TU_IP_RASPBERRY:8000"
   ```
5. Click **Deploy**

---

## 🌐 Configuración de Red

Para que Streamlit Cloud pueda acceder a tu Raspberry, tienes varias opciones:

### Opción 1: Tailscale (Recomendado - Seguro y fácil)

```bash
# En la Raspberry
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Obtén tu IP de Tailscale
tailscale ip -4
# Ejemplo: 100.x.x.x
```

Luego en Streamlit Cloud secrets:
```toml
BACKEND_API_URL = "http://100.x.x.x:8000"
```

### Opción 2: DuckDNS + Port Forwarding

```bash
# 1. Regístrate en duckdns.org y crea un dominio
# 2. Instala el cliente
mkdir ~/duckdns
cd ~/duckdns
nano duck.sh

# Contenido:
echo url="https://www.duckdns.org/update?domains=TU_DOMINIO&token=TU_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -

chmod 700 duck.sh
./duck.sh

# 3. Añade a cron
crontab -e
# Añadir: */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1

# 4. Configurar port forwarding en tu router
# Puerto externo: 8000 → IP Raspberry: 8000
```

### Opción 3: ngrok (Temporal - para pruebas)

```bash
# Instalar ngrok
sudo snap install ngrok

# Crear túnel
ngrok http 8000

# Copiar la URL (ej: https://xxxx.ngrok.io)
```

⚠️ **Importante**: Con ngrok free, la URL cambia cada vez que reinicias.

### Opción 4: VPN Wireguard (Avanzado)

[Guía oficial](https://www.wireguard.com/quickstart/)

---

## 📡 Endpoints de la API

### GET `/`
Health check básico
```bash
curl http://localhost:8000/
```

### GET `/health`
Estado detallado del sistema
```json
{
  "status": "healthy",
  "models_available": ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"],
  "capture_active": false,
  "timestamp": "2026-02-12T10:30:00"
}
```

### GET `/metrics`
Métricas del sistema (CPU, memoria, disco)
```json
{
  "cpu_percent": 45.2,
  "memory_percent": 62.8,
  "memory_available_mb": 1024.5,
  "disk_usage_percent": 38.1,
  "network_interfaces": ["lo", "eth0", "wlan0"],
  "timestamp": "2026-02-12T10:30:00"
}
```

### POST `/capture`
Captura paquetes de red

**Request:**
```json
{
  "duration": 60,
  "interface": null,
  "arp_filter_mode": "low"
}
```

**Response:**
```json
{
  "status": "success",
  "packets_captured": 1234,
  "data": [...],
  "duration_seconds": 60.2,
  "timestamp": "2026-02-12T10:31:00"
}
```

### POST `/predict`
Realiza predicción de anomalías

**Request:**
```json
{
  "data": [...],
  "model_name": "IFOREST",
  "metric_type": "Internas",
  "config": {
    "ae_normal_threshold": 0.60,
    "ocsvm_percentile": 0.45
  }
}
```

**Response:**
```json
{
  "status": "success",
  "predictions": [0, 0, 1, 0, ...],
  "n_normal": 1150,
  "n_anomalous": 84,
  "metrics": {
    "silhouette": 0.6234,
    "calinski_harabasz": 1234.56,
    "davies_bouldin": 0.4321
  },
  "timestamp": "2026-02-12T10:32:00"
}
```

### GET `/models`
Lista modelos disponibles
```json
{
  "available_models": ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"],
  "loaded": true,
  "model_paths": {...}
}
```

### POST `/reload-models`
Recarga modelos desde disco
```json
{
  "status": "success",
  "models_reloaded": ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"],
  "timestamp": "2026-02-12T10:33:00"
}
```

---

## 🧪 Testing

### Probar el backend localmente

```bash
# Terminal 1: Ejecutar backend
python backend_api.py

# Terminal 2: Probar endpoints
curl http://localhost:8000/health

# Captura de prueba (requiere tshark configurado)
curl -X POST http://localhost:8000/capture \
  -H "Content-Type: application/json" \
  -d '{"duration": 30, "arp_filter_mode": "low"}'
```

### Probar el frontend localmente

```bash
# Configurar variable de entorno
export BACKEND_API_URL="http://localhost:8000"

# Ejecutar frontend
streamlit run app_cloud.py
```

---

## 🐛 Troubleshooting

### Backend no inicia

**Error: `tshark: command not found`**
```bash
sudo apt install -y tshark
```

**Error: `Permission denied` al capturar**
```bash
sudo usermod -a -G wireshark $USER
newgrp wireshark
```

**Error: `Model file not found`**
```bash
# Verifica que estés en el directorio correcto
pwd
# Debe ser: /home/innovasic/Desktop/IDS para raspberry v2

ls model/
# Deben existir los archivos .pkl
```

### Frontend no conecta con backend

**Error: `Connection refused`**
- Verifica que el backend esté corriendo: `curl http://localhost:8000/health`
- Revisa el firewall: `sudo ufw status`
- Comprueba la IP correcta: `hostname -I`

**Error: `CORS error`**
- El backend ya tiene CORS habilitado con `allow_origins=["*"]`
- Si persiste, especifica el dominio exacto de Streamlit Cloud

**Error: `Timeout`**
- Aumenta el timeout en las requests del frontend
- Verifica la latencia: `ping TU_IP_RASPBERRY`

### Rendimiento

**Backend lento en Raspberry Pi 3**
- Reduce `duration` de captura
- Usa `arp_filter_mode='low'` o `'medium'`
- Considera actualizar a Raspberry Pi 4 (4GB+ RAM)

**Frontend lento**
- Streamlit Cloud ya debería ser rápido
- Si no, verifica que no estés haciendo `st.rerun()` en bucle

---

## 📊 Monitoreo

### Ver logs del backend

```bash
# Si usas systemd
sudo journalctl -u ids-backend -f

# Si ejecutas manualmente
# Los logs aparecen en la terminal
```

### Métricas de rendimiento

```python
# Endpoint de métricas cada 5 segundos
import time
while True:
    response = requests.get("http://localhost:8000/metrics")
    print(response.json())
    time.sleep(5)
```

---

## 🔒 Seguridad (Próximos Pasos)

### Añadir autenticación API Key

En `backend_api.py`:
```python
from fastapi import Header, HTTPException

API_KEY = "tu-clave-secreta"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.post("/capture", dependencies=[Depends(verify_api_key)])
async def capture_packets(...):
    ...
```

En `app_cloud.py`:
```python
headers = {"X-API-Key": os.getenv("API_KEY")}
response = requests.post(url, json=payload, headers=headers)
```

---

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Tailscale Setup](https://tailscale.com/kb/1017/install/)
- [DuckDNS](https://www.duckdns.org/)

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs del backend
2. Verifica la conectividad de red
3. Comprueba que los modelos estén cargados
4. Consulta esta documentación

**¡Listo! Ahora tienes un IDS IoT con arquitectura escalable y frontend fluido.** 🚀

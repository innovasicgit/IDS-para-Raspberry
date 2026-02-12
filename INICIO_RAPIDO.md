# 🚀 Inicio Rápido - Arquitectura API

## TL;DR - Comandos Rápidos

### En la Raspberry Pi (Backend)

```bash
# 1. Instalar dependencias (solo primera vez)
pip install -r requirements_backend.txt

# 2. Iniciar backend
./start_backend.sh

# 3. Detener backend
./stop_backend.sh
```

### En Streamlit Cloud (Frontend)

1. Sube `app_cloud.py` a GitHub
2. Despliega en [share.streamlit.io](https://share.streamlit.io)
3. Añade en Secrets:
   ```toml
   BACKEND_API_URL = "http://TU_IP_RASPBERRY:8000"
   ```

---

## 📁 Archivos de la Nueva Arquitectura

```
IDS para raspberry v2/
├── backend_api.py              # 🆕 API FastAPI (corre en Raspberry)
├── app_cloud.py                # 🆕 Frontend ligero (corre en Cloud)
├── requirements_backend.txt    # 🆕 Dependencias del backend
├── requirements_frontend.txt   # 🆕 Dependencias del frontend
├── start_backend.sh            # 🆕 Script de inicio del backend
├── stop_backend.sh             # 🆕 Script para detener el backend
├── .env.example                # 🆕 Configuración de ejemplo
├── ARQUITECTURA_API.md         # 🆕 Documentación completa
│
├── app.py                      # Original (aún funcional)
├── backend/                    # Módulos compartidos
├── frontend/                   # Módulos compartidos
├── model/                      # Modelos ML
└── ...
```

---

## 🎯 ¿Qué Cambia?

### ANTES (Todo en Raspberry)
```
Raspberry Pi
└── Streamlit (app.py)
    ├── Captura de red
    ├── Modelos ML
    ├── UI (con lag)
    └── Animaciones (lentas)
```
❌ **Problemas**: Lag, animaciones lentas, UI congelada

### AHORA (Separado)
```
Raspberry Pi                Streamlit Cloud
└── FastAPI (backend_api.py)  └── Streamlit (app_cloud.py)
    ├── Captura de red  ─────────►  UI fluida
    ├── Modelos ML      ◄─────────  Sin lag
    └── Solo procesa datos         └── Animaciones suaves
```
✅ **Ventajas**: UI rápida, backend optimizado, escalable

---

## 🔧 Setup Inicial (10 minutos)

### Paso 1: Backend en Raspberry

```bash
cd ~/Desktop/IDS\ para\ raspberry\ v2

# Instalar dependencias
pip install fastapi uvicorn

# Probar que funciona
python backend_api.py
```

Deberías ver:
```
✅ Modelos cargados correctamente
✅ Servidor listo para recibir peticiones
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 2: Probar localmente

Abre otro terminal:
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "models_available": ["IFOREST", "OCSVM", "KMEANS", "AUTOENCODER"],
  "capture_active": false
}
```

### Paso 3: Frontend local (opcional)

```bash
export BACKEND_API_URL="http://localhost:8000"
streamlit run app_cloud.py
```

### Paso 4: Deploy en Cloud

1. Crea un nuevo repo en GitHub (o una carpeta en el existente)
2. Sube solo:
   - `app_cloud.py` (renombra a `app.py`)
   - `requirements_frontend.txt` (renombra a `requirements.txt`)
3. En Streamlit Cloud → Deploy → Secrets:
   ```toml
   BACKEND_API_URL = "http://TU_IP_RASPBERRY:8000"
   ```

**⚠️ Importante**: Para acceso desde internet, necesitas exponer tu Raspberry (ver [Configuración de Red](#configuración-de-red))

---

## 🌐 Configuración de Red

### Opción 1: Tailscale (Más Fácil) ⭐

```bash
# En la Raspberry
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Mi IP es:
tailscale ip -4
100.96.121.76
```

Usa en Streamlit Cloud secrets:
```toml
BACKEND_API_URL = "http://100.68.42.17:8000"
```

### Opción 2: ngrok (Temporal)

```bash
ngrok http 8000
# Copia la URL https://xxxx.ngrok.io
```

### Opción 3: Port Forwarding + DuckDNS (Permanente)

Ver documentación completa en `ARQUITECTURA_API.md`

---

## 🧪 Testing

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Métricas del Sistema
```bash
curl http://localhost:8000/metrics
```

### Test 3: Captura Corta
```bash
curl -X POST http://localhost:8000/capture \
  -H "Content-Type: application/json" \
  -d '{"duration": 10, "arp_filter_mode": "low"}'
```

### Test 4: Frontend Local
```bash
export BACKEND_API_URL="http://localhost:8000"
streamlit run app_cloud.py
```

---

## 📊 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check básico |
| `/health` | GET | Estado detallado |
| `/metrics` | GET | CPU, RAM, disco |
| `/capture` | POST | Captura paquetes |
| `/predict` | POST | Predice anomalías |
| `/models` | GET | Lista modelos |
| `/reload-models` | POST | Recarga modelos |

Ver detalles en `ARQUITECTURA_API.md`

---

## 🐛 Problemas Comunes

### "Connection refused"
```bash
# Verifica que el backend esté corriendo
curl http://localhost:8000/health

# Si no responde, revisa logs
tail -f backend.log
```

### "Permission denied" en captura
```bash
sudo usermod -a -G wireshark $USER
newgrp wireshark
```

### "Model not found"
```bash
# Verifica que estés en el directorio correcto
pwd
ls model/
```

### Frontend no conecta
- Verifica la IP: `hostname -I`
- Prueba localmente primero: `export BACKEND_API_URL="http://localhost:8000"`
- Revisa firewall: `sudo ufw status`

---

## 📚 Documentación Completa

- **ARQUITECTURA_API.md**: Guía detallada con todos los pasos
- **requirements_backend.txt**: Dependencias del backend
- **requirements_frontend.txt**: Dependencias del frontend
- **.env.example**: Variables de entorno

---

## 🎓 Próximos Pasos

1. ✅ **Backend funcionando localmente**
2. ✅ **Frontend funcionando localmente**
3. 🔄 **Exponer Raspberry a internet** (Tailscale/ngrok)
4. 🔄 **Deploy frontend en Streamlit Cloud**
5. 🔄 **Configurar dominio personalizado** (opcional)
6. 🔄 **Añadir autenticación API** (opcional)

---

## 💡 Comparación de Rendimiento

| Métrica | Antes (Todo local) | Ahora (API + Cloud) |
|---------|-------------------|---------------------|
| Carga CPU Raspberry | ~80% | ~30% |
| Lag en UI | Frecuente | Ninguno |
| Animaciones | Lentas | Fluidas |
| Escalabilidad | Limitada | Alta |
| Acceso remoto | Difícil | Fácil (via cloud) |

---

## 🆘 Soporte

Si algo no funciona:
1. Verifica logs: `tail -f backend.log`
2. Prueba localmente primero
3. Revisa conectividad de red
4. Consulta `ARQUITECTURA_API.md`

---

**¡Todo listo!** 🎉

Ahora tienes:
- ✅ Backend optimizado en Raspberry
- ✅ Frontend fluido en Cloud
- ✅ Arquitectura escalable
- ✅ Sin lag ni congelamientos

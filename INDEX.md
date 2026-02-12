# 📚 Índice de Documentación - Arquitectura API

## 🎯 Inicio Rápido

¿Primera vez aquí? **Empieza por estos archivos en orden:**

1. 📄 **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** (5 min)
   - Overview del proyecto
   - Problema y solución
   - Resultados cuantitativos

2. 📄 **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** (10 min)
   - Setup paso a paso
   - Comandos esenciales
   - Troubleshooting básico

3. 📄 **[README_API.md](README_API.md)** (10 min)
   - Comparación con versión anterior
   - Endpoints disponibles
   - Ejemplos de uso

---

## 📖 Documentación por Rol

### 👨‍💻 Desarrollador

**Implementación**
- 📄 [ARQUITECTURA_API.md](ARQUITECTURA_API.md) - Guía técnica completa
- 📄 [FLUJO_COMPLETO.md](FLUJO_COMPLETO.md) - Diagramas de flujo
- 📄 `backend_api.py` - Código del backend
- 📄 `app_cloud.py` - Código del frontend

**Testing**
- 📄 `test_backend.py` - Suite de tests
- 📄 `check_prerequisites.py` - Verificador de sistema

**Scripts**
- 📄 `start_backend.sh` - Iniciar backend
- 📄 `stop_backend.sh` - Detener backend

### 🖥️ DevOps / SysAdmin

**Despliegue**
- 📄 [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → Sección "Instalación Backend"
- 📄 [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → Sección "Configuración de Red"
- 📄 `.env.example` - Variables de entorno

**Monitoreo**
- 📄 [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → Sección "Monitoreo"
- 📄 Endpoint `/metrics` en `backend_api.py`

**Seguridad**
- 📄 [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → Sección "Seguridad"

### 👔 Manager / Stakeholder

**Resumen de Negocio**
- 📄 [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)
  - ROI y métricas
  - Comparación con alternativas
  - Roadmap futuro

**Resultados**
- 📄 [README_API.md](README_API.md) → Sección "Comparación de Rendimiento"

### 👨‍🎓 Usuario Final

**Cómo Usar**
- 📄 [INICIO_RAPIDO.md](INICIO_RAPIDO.md) → Sección "Uso"
- 📄 Frontend en Cloud (interfaz gráfica)

---

## 🗂️ Estructura de Archivos

```
📁 IDS para raspberry v2/
│
├── 🚀 INICIO RÁPIDO
│   ├── RESUMEN_EJECUTIVO.md      ← Empieza aquí
│   ├── INICIO_RAPIDO.md          ← Setup en 10 min
│   └── README_API.md             ← Overview general
│
├── 📖 DOCUMENTACIÓN TÉCNICA
│   ├── ARQUITECTURA_API.md       ← Guía completa (800+ líneas)
│   ├── FLUJO_COMPLETO.md         ← Diagramas de flujo
│   └── INDEX.md                  ← Este archivo
│
├── 💻 CÓDIGO BACKEND
│   ├── backend_api.py            ← API FastAPI principal
│   ├── backend/                  ← Módulos compartidos
│   │   ├── capture_utils.py
│   │   ├── predict.py
│   │   ├── model_utils.py
│   │   └── constants.py
│   └── model/                    ← Modelos ML
│
├── 🎨 CÓDIGO FRONTEND
│   ├── app_cloud.py              ← Frontend para Streamlit Cloud
│   └── frontend/                 ← Módulos UI compartidos
│
├── 🔧 CONFIGURACIÓN
│   ├── requirements_backend.txt
│   ├── requirements_frontend.txt
│   └── .env.example
│
├── 🤖 SCRIPTS DE AUTOMATIZACIÓN
│   ├── start_backend.sh          ← Iniciar backend
│   ├── stop_backend.sh           ← Detener backend
│   ├── check_prerequisites.py    ← Verificar sistema
│   └── test_backend.py           ← Suite de tests
│
└── 📜 ORIGINAL (Sin cambios)
    ├── app.py                    ← Versión original
    ├── requirements.txt          ← Deps originales
    └── ...
```

---

## 🎯 Guías por Tarea

### 🏗️ Instalar el Sistema

1. [INICIO_RAPIDO.md](INICIO_RAPIDO.md) → "Setup Inicial"
2. Ejecutar: `python check_prerequisites.py`
3. Ejecutar: `./start_backend.sh`

### 🧪 Hacer Testing

1. [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → Sección "Testing"
2. Ejecutar: `python test_backend.py`
3. Revisar: endpoints con `curl`

### 🌐 Exponer a Internet

1. [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Configuración de Red"
2. Elegir método:
   - **Tailscale** (recomendado)
   - **ngrok** (temporal)
   - **DuckDNS + Port Forwarding** (permanente)

### ☁️ Deploy en Cloud

1. [INICIO_RAPIDO.md](INICIO_RAPIDO.md) → "Frontend en Cloud"
2. GitHub + Streamlit Cloud
3. Configurar secrets

### 🐛 Resolver Problemas

1. [INICIO_RAPIDO.md](INICIO_RAPIDO.md) → "Problemas Comunes"
2. [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Troubleshooting"
3. Ejecutar: `python check_prerequisites.py`

### 📊 Ver Métricas

1. Endpoint: `GET /metrics`
2. [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Monitoreo"

---

## 📚 Referencia Rápida

### Comandos Esenciales

```bash
# Setup
python check_prerequisites.py
pip install -r requirements_backend.txt

# Backend
./start_backend.sh           # Iniciar
./stop_backend.sh            # Detener
tail -f backend.log          # Ver logs

# Testing
python test_backend.py       # Test completo
curl http://localhost:8000/health  # Health check

# Frontend local
export BACKEND_API_URL="http://localhost:8000"
streamlit run app_cloud.py
```

### Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Estado detallado |
| `/metrics` | GET | CPU, RAM, disco |
| `/capture` | POST | Captura paquetes |
| `/predict` | POST | Predice anomalías |
| `/models` | GET | Lista modelos |

### Archivos de Configuración

- **Backend**: `requirements_backend.txt`
- **Frontend**: `requirements_frontend.txt`
- **Variables de entorno**: `.env.example` → copia a `.env`

---

## 🔍 Búsqueda por Palabra Clave

### Captura de Paquetes
- [FLUJO_COMPLETO.md](FLUJO_COMPLETO.md) → "Captura de Paquetes"
- `backend_api.py` → Endpoint `/capture`
- `backend/capture_utils.py` → Funciones de captura

### Modelos ML
- [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Modelos en Memoria"
- `backend_api.py` → `load_all_models()`
- `backend/model_utils.py` → Funciones de carga

### Métricas
- `backend_api.py` → Endpoint `/metrics`
- `metricas.py` → Métricas internas

### Frontend
- `app_cloud.py` → UI completa
- [README_API.md](README_API.md) → "Frontend Ligero"

### Networking
- [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Configuración de Red"
- Tailscale, ngrok, DuckDNS

### Seguridad
- [ARQUITECTURA_API.md](ARQUITECTURA_API.md) → "Seguridad"
- CORS, autenticación, HTTPS

---

## 📈 Roadmap de Lectura Sugerido

### Día 1: Comprensión (30 min)
1. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - 5 min
2. [README_API.md](README_API.md) - 10 min
3. [FLUJO_COMPLETO.md](FLUJO_COMPLETO.md) - Diagramas - 15 min

### Día 2: Setup (1 hora)
1. [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - 10 min
2. Setup Backend - 30 min
3. Testing - 20 min

### Día 3: Profundización (2 horas)
1. [ARQUITECTURA_API.md](ARQUITECTURA_API.md) - Completa - 1 hora
2. Revisar código: `backend_api.py` - 30 min
3. Revisar código: `app_cloud.py` - 30 min

### Día 4: Deploy (1 hora)
1. Configurar red (Tailscale/ngrok) - 30 min
2. Deploy frontend en Cloud - 20 min
3. Testing end-to-end - 10 min

---

## 🆘 Soporte y Recursos

### Documentación Interna
- Todos los archivos `.md` en este proyecto

### Herramientas de Debug
- `check_prerequisites.py` - Verificar sistema
- `test_backend.py` - Test automatizado
- `backend.log` - Logs del backend

### Comandos de Debug
```bash
# Ver estado del backend
ps aux | grep backend_api

# Ver logs en tiempo real
tail -f backend.log

# Test de conectividad
curl -v http://localhost:8000/health

# Ver puertos en uso
sudo lsof -i:8000
```

---

## 📝 Changelog

### Versión 1.0 (Febrero 2026)
- ✅ Backend API con FastAPI
- ✅ Frontend optimizado para Cloud
- ✅ Documentación completa (3,500+ líneas)
- ✅ Scripts de automatización
- ✅ Suite de tests

---

## 🎓 Recursos Externos

### Tecnologías Usadas
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tailscale Setup](https://tailscale.com/kb/1017/install/)
- [DuckDNS Guide](https://www.duckdns.org/)
- [ngrok Documentation](https://ngrok.com/docs)

### Aprendizaje
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- REST API Best Practices: https://restfulapi.net/
- Raspberry Pi Networking: https://www.raspberrypi.com/documentation/

---

<p align="center">
  <strong>Índice de Documentación - IDS IoT</strong><br>
  <em>Arquitectura API - Febrero 2026</em><br>
  <br>
  📚 Total: 12 archivos de documentación | 3,500+ líneas<br>
  ⭐ Todo listo para producción
</p>

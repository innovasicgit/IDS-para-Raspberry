# 🔄 Flujo de Trabajo Completo

## 📋 Diagrama de Flujo: Desde Instalación hasta Uso

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: INSTALACIÓN                       │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────┐
         │ 1. Verificar Prerequisitos        │
         │    python check_prerequisites.py  │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ 2. Instalar Dependencias          │
         │    pip install -r                 │
         │    requirements_backend.txt       │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ 3. Configurar tshark              │
         │    sudo usermod -a -G             │
         │    wireshark $USER                │
         └───────────┬───────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASE 2: CONFIGURACIÓN                     │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ 4. Elegir Método de Exposición    │
         └───────────┬───────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌─────────┐
    │Tailscale│ │ ngrok  │  │DuckDNS+ │
    │ (VPN)  │  │(Túnel) │  │Port Fwd │
    └────┬───┘  └────┬───┘  └────┬────┘
         │           │            │
         └───────────┼────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ 5. Obtener URL/IP del Backend     │
         │    Ejemplo:                       │
         │    • http://100.x.x.x:8000        │
         │    • https://xxx.ngrok.io         │
         │    • http://mi-pi.duckdns.org     │
         └───────────┬───────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASE 3: DEPLOYMENT                        │
└─────────────────────────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  BACKEND (Pi)    │    │ FRONTEND (Cloud) │
│                  │    │                  │
│ ./start_backend  │    │ 1. GitHub        │
│                  │    │ 2. Streamlit     │
│ Puerto: 8000     │    │ 3. Secrets:      │
│                  │    │    BACKEND_API   │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASE 4: TESTING                          │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Test Backend Local                │
         │ python test_backend.py            │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Test Frontend Local               │
         │ export BACKEND_API_URL=...        │
         │ streamlit run app_cloud.py        │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Test Conectividad End-to-End      │
         │ Frontend Cloud → Backend Pi       │
         └───────────┬───────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASE 5: USO                             │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Usuario accede al Frontend        │
         │ https://tu-app.streamlit.app      │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Inicia Captura desde UI           │
         │ • Duración: 60s                   │
         │ • Filtro ARP: low                 │
         │ • Modelo: IFOREST                 │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Frontend → POST /capture          │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Backend captura paquetes          │
         │ (tshark en eth0/wlan0)            │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Backend → Response con datos      │
         │ {packets_captured: 1234, data:..} │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Frontend → POST /predict          │
         │ {data:..., model_name:"IFOREST"}  │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Backend ejecuta modelo ML         │
         │ • Limpia datos                    │
         │ • Carga modelo                    │
         │ • Predice anomalías               │
         │ • Calcula métricas                │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Backend → Response con predicción │
         │ {predictions:[0,0,1,0],           │
         │  n_normal:1150, n_anomalous:84}   │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ Frontend muestra resultados       │
         │ • Gráfico de pie                  │
         │ • Métricas                        │
         │ • Tablas                          │
         └───────────┬───────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────┐
         │ ✅ Ciclo completo                 │
         │ Usuario puede repetir análisis    │
         └───────────────────────────────────┘
```

---

## 🔄 Flujo Técnico Detallado

### 1. Captura de Paquetes

```
Usuario (Frontend)
    │
    │ POST /capture {duration: 60}
    ▼
Backend API
    │
    ├─► build_tshark_command()
    │   └─► Construye comando con filtros
    │
    ├─► capturing_packets(command)
    │   └─► Inicia proceso tshark
    │
    ├─► Loop por 60 segundos:
    │   ├─► Lee stdout de tshark
    │   ├─► type_packet(line)
    │   │   └─► Parsea campos
    │   └─► packet_df(packet_dict, df)
    │       └─► Acumula en DataFrame
    │
    ├─► apply_arp_filter(df)
    │   └─► Limita paquetes ARP
    │
    └─► Response {status, packets_captured, data}
        │
        ▼
Frontend
    └─► Muestra "✅ 1234 paquetes capturados"
```

### 2. Predicción de Anomalías

```
Frontend
    │
    │ POST /predict {data, model_name}
    ▼
Backend API
    │
    ├─► pd.DataFrame(data)
    │   └─► Convierte JSON a DataFrame
    │
    ├─► clean_data(df)
    │   ├─► Replace NaN
    │   ├─► del_columns()
    │   ├─► Convert tipos
    │   └─► Fillna(0)
    │
    ├─► MODELS_CACHE[model_name]
    │   └─► Obtiene modelo pre-cargado
    │
    ├─► predecir(model, df_clean, model_name)
    │   ├─► Si IFOREST: decision_function + threshold
    │   ├─► Si OCSVM: predict con signo
    │   ├─► Si KMEANS: predict directo
    │   └─► Si AUTOENCODER: proba + reconstruction_error
    │
    ├─► metrica_internas(df, predictions)
    │   ├─► silhouette_score
    │   ├─► calinski_harabasz_score
    │   └─► davies_bouldin_score
    │
    └─► Response {predictions, n_normal, n_anomalous, metrics}
        │
        ▼
Frontend
    ├─► Gráfico Pie (Normal vs Anomalías)
    ├─► Métricas (Silhouette, Calinski, Davies)
    └─► Tabla de datos
```

---

## 🔐 Flujo de Seguridad (Futuro)

```
Frontend
    │
    │ Headers: {"X-API-Key": "secret123"}
    ▼
Backend API
    │
    ├─► verify_api_key(x_api_key)
    │   ├─► if key != stored_key:
    │   │   └─► HTTPException(401)
    │   └─► else: continue
    │
    └─► Ejecuta endpoint normalmente
```

---

## 📊 Flujo de Datos

```
┌──────────────┐
│ Interfaces   │
│ eth0, wlan0  │
└──────┬───────┘
       │ Paquetes raw
       ▼
┌──────────────┐
│   tshark     │
│ (captura)    │
└──────┬───────┘
       │ Texto plano (TSV)
       ▼
┌──────────────┐
│ type_packet  │
│ (parseo)     │
└──────┬───────┘
       │ Dict Python
       ▼
┌──────────────┐
│ packet_df    │
│ (acumulación)│
└──────┬───────┘
       │ DataFrame
       ▼
┌──────────────┐
│ clean_data   │
│ (limpieza)   │
└──────┬───────┘
       │ DataFrame limpio
       ▼
┌──────────────┐
│ Modelo ML    │
│ (predicción) │
└──────┬───────┘
       │ Array de 0/1
       ▼
┌──────────────┐
│ metricas     │
│ (evaluación) │
└──────┬───────┘
       │ Scores
       ▼
┌──────────────┐
│ Response JSON│
│ (al frontend)│
└──────────────┘
```

---

## 🔄 Ciclo de Vida del Backend

```
┌─────────────────────────────────────┐
│        STARTUP                      │
│  • Carga modelos ML                 │
│  • Inicializa FastAPI               │
│  • Bind puerto 8000                 │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│        IDLE                         │
│  • Espera requests                  │
│  • Monitorea recursos               │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│     PROCESSING REQUEST              │
│  • Recibe POST /capture             │
│  • Captura paquetes                 │
│  • Envía response                   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│        IDLE                         │
│  • Espera siguiente request         │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│     PROCESSING REQUEST              │
│  • Recibe POST /predict             │
│  • Ejecuta modelo                   │
│  • Envía response                   │
└──────────┬──────────────────────────┘
           │
           ▼
        (ciclo continúa...)
           │
           ▼
┌─────────────────────────────────────┐
│        SHUTDOWN                     │
│  • Ctrl+C o kill                    │
│  • Cleanup de recursos              │
└─────────────────────────────────────┘
```

---

## 🎯 Puntos Clave

### ✅ Ventajas de la Arquitectura

1. **Separación de Responsabilidades**
   - Backend: Solo procesamiento pesado
   - Frontend: Solo UI/UX

2. **Escalabilidad**
   - Un backend puede servir múltiples frontends
   - Fácil añadir balanceadores de carga

3. **Mantenimiento**
   - Actualiza frontend sin tocar backend
   - Actualiza modelos sin redesplegar frontend

4. **Performance**
   - Frontend en cloud: recursos ilimitados
   - Backend en local: acceso directo a red

### ⚠️ Consideraciones

1. **Latencia de Red**
   - Depende de la conexión Raspberry ↔ Cloud
   - Mitigación: Tailscale o VPN de baja latencia

2. **Seguridad**
   - Exponer Raspberry a internet tiene riesgos
   - Recomendado: Tailscale (VPN privada)
   - Alternativa: Autenticación API Key

3. **Disponibilidad**
   - Si la Raspberry se apaga, frontend no funciona
   - Considerar: UPS, servicio systemd, monitoreo

---

## 📚 Recursos Adicionales

- **INICIO_RAPIDO.md**: Setup paso a paso
- **ARQUITECTURA_API.md**: Documentación técnica completa
- **README_API.md**: Overview y comandos útiles
- **check_prerequisites.py**: Verificación automática
- **test_backend.py**: Suite de tests

---

<p align="center">
  <strong>Diagrama creado para el proyecto IDS IoT</strong><br>
  <em>Arquitectura API - Febrero 2026</em>
</p>

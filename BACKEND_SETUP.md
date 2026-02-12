# Configuración del Backend para Captura de Paquetes

## Problema Resuelto

La captura automática de paquetes requiere `tshark` que solo está disponible en la Raspberry Pi, no en Streamlit Cloud. La solución implementada:

- **En Streamlit Cloud**: El frontend llama al backend API en Raspberry Pi para capturar paquetes
- **En local**: El frontend usa tshark directamente

## Configuración en Streamlit Cloud

Para que la captura funcione en Streamlit Cloud, debes configurar el secret `BACKEND_URL`:

### Pasos:

1. Ve a tu app en https://share.streamlit.io/
2. Click en "⚙️ Settings" → "Secrets"
3. Agrega el siguiente contenido:

```toml
BACKEND_URL = "https://reviewed-sailing-grid-clinic.trycloudflare.com"
```

4. Click en "Save"
5. La app se reiniciará automáticamente

### Actualizar la URL del Backend

Si cambias el túnel de Cloudflare o usas otro método de exposición:

1. Actualiza el secret `BACKEND_URL` en Streamlit Cloud
2. Guarda los cambios

## Configuración Local

Para desarrollo local, crea el archivo `.streamlit/secrets.toml` (ya está en `.gitignore`):

```toml
BACKEND_URL = "http://localhost:8000"
```

O si usas Tailscale:

```toml
BACKEND_URL = "http://100.96.121.76:8000"
```

## Verificación del Backend

Antes de usar la captura, verifica que el backend esté corriendo:

```bash
# En la Raspberry Pi
curl https://reviewed-sailing-grid-clinic.trycloudflare.com/health
```

Debería responder:

```json
{
  "status": "healthy",
  "timestamp": "..."
}
```

## Funcionalidades Implementadas

### Captura Manual
- Duración configurable en minutos
- Llama a `/capture` endpoint del backend
- Muestra los paquetes capturados

### Captura Automática
- Duración de cada captura configurable
- Intervalo entre capturas configurable
- Ejecuta predicción automática después de cada captura
- Contador regresivo para la próxima captura

## Troubleshooting

### Error: "Error de conexión al backend"

**Causa**: El backend no está accesible

**Solución**:
1. Verifica que el túnel de Cloudflare esté activo en la Raspberry Pi
2. Verifica que el backend API esté corriendo: `ps aux | grep uvicorn`
3. Reinicia el backend: `./start_backend.sh`

### Error: "No se capturaron paquetes"

**Causa**: No hay tráfico en la red o interfaces incorrectas

**Solución**:
1. Verifica que haya tráfico en la red
2. En la Raspberry Pi, revisa las interfaces: `sudo tshark -D`
3. Ajusta las interfaces en `backend/capture_utils.py` (línea 7)

### La captura es muy lenta

**Causa**: Latencia de red entre Streamlit Cloud y Raspberry Pi

**Solución**:
- Usa duraciones más largas (2-5 minutos mínimo)
- Considera usar CSV pre-capturados para testing

## Arquitectura

```
┌─────────────────┐         HTTPS          ┌──────────────────┐
│                 │ ───────────────────────>│                  │
│ Streamlit Cloud │                         │   Raspberry Pi   │
│   (Frontend)    │                         │    (Backend)     │
│                 │ <───────────────────────│                  │
└─────────────────┘      JSON Response      └──────────────────┘
                                                      │
                                                      │ tshark
                                                      ▼
                                               ┌─────────────┐
                                               │   Network   │
                                               │  Interface  │
                                               └─────────────┘
```

## Endpoints del Backend

- `POST /capture` - Captura paquetes
  - Parámetros: `duration` (segundos), `arp_filter_mode`
  - Respuesta: JSON con paquetes capturados

- `POST /predict` - Ejecuta predicción
  - Parámetros: `data`, `model`
  - Respuesta: JSON con resultados

- `GET /health` - Verificar estado del backend
- `GET /metrics` - Métricas del sistema

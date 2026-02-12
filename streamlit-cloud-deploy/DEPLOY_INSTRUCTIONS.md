# 🚀 Instrucciones de Deploy en Streamlit Cloud

## Paso 1: Preparar el Backend en Raspberry Pi

Antes de desplegar el frontend, asegúrate que el backend esté funcionando:

```bash
cd ~/Desktop/IDS\ para\ raspberry\ v2
./start_backend.sh
```

Verificar que está corriendo:
```bash
curl http://localhost:8000/health
```

Deberías ver:
```json
{"status": "healthy", "timestamp": "..."}
```

## Paso 2: Verificar Tailscale

Tu Raspberry Pi debe estar conectada a Tailscale:

```bash
tailscale status
```

Tu IP Tailscale es: **100.96.121.76**

Verifica que el backend sea accesible desde otra máquina en tu red Tailscale:
```bash
curl http://100.96.121.76:8000/health
```

## Paso 3: Deploy en Streamlit Cloud

### 3.1 Crear Cuenta

1. Ve a https://share.streamlit.io
2. Inicia sesión con GitHub

### 3.2 Crear Nueva App

1. Click en **"New app"**
2. Configurar:
   - **Repository**: `innovasicgit/IDS-para-Raspberry`
   - **Branch**: `main`
   - **Main file path**: `streamlit-cloud-deploy/app.py`

### 3.3 Configurar Secrets

En la sección **Advanced settings** → **Secrets**, agregar:

```toml
BACKEND_API_URL = "http://100.96.121.76:8000"
```

⚠️ **IMPORTANTE**: Usa tu IP de Tailscale correcta (100.96.121.76)

### 3.4 Deploy

Click en **"Deploy!"**

La app estará disponible en:
```
https://[tu-username]-ids-para-raspberry-[random].streamlit.app
```

## Paso 4: Verificar Funcionamiento

1. **Abrir la app** en tu navegador
2. **Verificar conexión al backend**: Deberías ver el estado "🟢 Conectado"
3. **Probar captura**: Click en "📡 Capturar Tráfico"
4. **Verificar predicción**: Deberías ver análisis de tráfico y anomalías

## 🔧 Troubleshooting

### Error: "Cannot connect to backend"

**Causa**: El frontend no puede alcanzar el backend.

**Soluciones**:
1. Verifica que el backend esté corriendo en la Raspberry Pi
2. Verifica que Tailscale esté activo en ambos dispositivos
3. Prueba acceder a `http://100.96.121.76:8000/health` desde tu navegador

### Error: "Backend API timeout"

**Causa**: El backend está lento o no responde.

**Soluciones**:
1. Reinicia el backend: `./stop_backend.sh && ./start_backend.sh`
2. Verifica recursos del sistema: `./check_prerequisites.py`

### Error: "Model not found"

**Causa**: Los modelos ML no están cargados.

**Soluciones**:
1. Verifica que los modelos existan en `model/`
2. Recarga modelos: `curl http://100.96.121.76:8000/reload-models`

## 📊 Monitoreo

### Ver logs del backend

```bash
tail -f ~/Desktop/IDS\ para\ raspberry\ v2/backend.log
```

### Ver métricas del sistema

```bash
cd ~/Desktop/IDS\ para\ raspberry\ v2
python3 generate_report.py
```

## 🔐 Seguridad

### Buenas Prácticas

1. **No exponer el backend públicamente**: Solo usar Tailscale
2. **Rotar secrets regularmente**: Cambiar `BACKEND_API_URL` si cambia la IP
3. **Monitorear accesos**: Revisar logs del backend

### Actualizar Secrets

Si cambias la IP de Tailscale:

1. Ve a tu app en Streamlit Cloud
2. Settings → Secrets
3. Actualizar `BACKEND_API_URL`
4. Reiniciar app

## 🔄 Actualizar la App

### Hacer cambios

1. Editar `app.py` localmente
2. Commit y push a GitHub:
   ```bash
   git add streamlit-cloud-deploy/
   git commit -m "Update frontend"
   git push origin main
   ```
3. Streamlit Cloud auto-desplegará los cambios

### Rollback

Si algo falla:

1. Ve a Streamlit Cloud
2. Settings → Manage app
3. Click en "Reboot app" o "Delete app"

## 📞 Soporte

Si tienes problemas:

1. Revisar logs: `tail -f backend.log`
2. Verificar prerequisitos: `./check_prerequisites.py`
3. Generar reporte: `python3 generate_report.py`

---

## ✅ Checklist de Deploy

- [ ] Backend corriendo en Raspberry Pi
- [ ] Tailscale activo (IP: 100.96.121.76)
- [ ] Backend responde en `/health`
- [ ] Código subido a GitHub
- [ ] App creada en Streamlit Cloud
- [ ] Secrets configurados
- [ ] App desplegada exitosamente
- [ ] Frontend conecta al backend
- [ ] Captura de tráfico funciona
- [ ] Predicción de anomalías funciona

---

**🎉 ¡Listo para producción!**

# Deploy en Streamlit Cloud

Esta carpeta contiene todo lo necesario para desplegar el frontend del IDS IoT en Streamlit Cloud.

## 📋 Contenido

- `app.py` - Aplicación Streamlit (frontend ligero)
- `requirements.txt` - Dependencias Python
- `.streamlit/config.toml` - Configuración de tema
- `DEPLOY_INSTRUCTIONS.md` - Instrucciones paso a paso
- `LISTO_PARA_DEPLOY.txt` - Checklist de verificación

## 🚀 Deploy Rápido

1. **Subir a GitHub** (este paso)
2. **Ir a Streamlit Cloud**: https://share.streamlit.io
3. **Crear nueva app**:
   - Repository: `innovasicgit/IDS-para-Raspberry`
   - Branch: `main`
   - Main file path: `streamlit-cloud-deploy/app.py`
4. **Configurar Secrets**:
   ```toml
   BACKEND_API_URL = "http://100.96.121.76:8000"
   ```
5. **Deploy!** ✨

## 🔧 Configuración del Backend

Antes de usar el frontend, asegúrate que el backend esté corriendo en tu Raspberry Pi:

```bash
cd ~/Desktop/IDS\ para\ raspberry\ v2
./start_backend.sh
```

## 📡 Conexión

- Backend API: `http://100.96.121.76:8000` (vía Tailscale)
- Frontend Cloud: `https://tu-app.streamlit.app`

## 🔐 Seguridad

- La conexión usa Tailscale VPN
- No se exponen puertos públicos
- Autenticación en el backend

---

Para más detalles, ver `DEPLOY_INSTRUCTIONS.md`

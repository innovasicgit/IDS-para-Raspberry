#!/bin/bash
# ============================================================
# IDS para Raspberry Pi — Script de inicio automático
# Inicia Streamlit + Cloudflare Tunnel
# ============================================================

PROJECT_DIR="/home/innovasic/Desktop/IDS para raspberry v2"
VENV_DIR="$PROJECT_DIR/nuevoEntorno"
LOG_DIR="$PROJECT_DIR/logs"
STREAMLIT_PORT=8501

# Crear directorio de logs si no existe
mkdir -p "$LOG_DIR"

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   🛡️  IDS para Raspberry Pi — Inicio      ${NC}"
echo -e "${BLUE}============================================${NC}"

# 1. Matar procesos anteriores
echo -e "${YELLOW}[1/4]${NC} Deteniendo procesos anteriores..."
pkill -f "streamlit run" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 2

# 2. Iniciar Streamlit
echo -e "${YELLOW}[2/4]${NC} Iniciando Streamlit..."
cd "$PROJECT_DIR"
source "$VENV_DIR/bin/activate"
nohup streamlit run app.py \
    --server.port "$STREAMLIT_PORT" \
    --server.address 0.0.0.0 \
    --server.headless true \
    > "$LOG_DIR/streamlit.log" 2>&1 &

# Esperar a que Streamlit esté listo
echo -n "       Esperando Streamlit"
for i in $(seq 1 15); do
    if curl -s -o /dev/null -w "" http://localhost:$STREAMLIT_PORT 2>/dev/null; then
        echo ""
        echo -e "       ${GREEN}✅ Streamlit activo en puerto $STREAMLIT_PORT${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Verificar que arrancó
if ! curl -s -o /dev/null http://localhost:$STREAMLIT_PORT 2>/dev/null; then
    echo ""
    echo -e "       ${RED}❌ Streamlit no arrancó. Revisa: $LOG_DIR/streamlit.log${NC}"
    exit 1
fi

# 3. Iniciar Cloudflare Tunnel
echo -e "${YELLOW}[3/4]${NC} Iniciando Cloudflare Tunnel..."
nohup cloudflared tunnel --url http://localhost:$STREAMLIT_PORT \
    > "$LOG_DIR/cloudflared.log" 2>&1 &

# Esperar a que el túnel genere la URL
echo -n "       Esperando túnel"
TUNNEL_URL=""
for i in $(seq 1 20); do
    TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' "$LOG_DIR/cloudflared.log" 2>/dev/null | head -1)
    if [ -n "$TUNNEL_URL" ]; then
        echo ""
        break
    fi
    echo -n "."
    sleep 1
done

# 4. Mostrar resultado
echo -e "${YELLOW}[4/4]${NC} Resultado:"
echo ""

if [ -n "$TUNNEL_URL" ]; then
    # Guardar URL en archivo para referencia
    echo "$TUNNEL_URL" > "$LOG_DIR/tunnel_url.txt"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $TUNNEL_URL" >> "$LOG_DIR/tunnel_history.txt"
    
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   ✅ IDS ACTIVO Y PÚBLICO                  ${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo -e "   🏠 Local:   ${BLUE}http://localhost:$STREAMLIT_PORT${NC}"
    echo -e "   🌐 Público: ${BLUE}$TUNNEL_URL${NC}"
    echo ""
    echo -e "   📋 URL copiada en: ${YELLOW}$LOG_DIR/tunnel_url.txt${NC}"
    echo -e "   📝 Logs Streamlit: ${YELLOW}$LOG_DIR/streamlit.log${NC}"
    echo -e "   📝 Logs Tunnel:    ${YELLOW}$LOG_DIR/cloudflared.log${NC}"
    echo ""
    echo -e "${GREEN}============================================${NC}"
else
    echo -e "${RED}❌ No se pudo obtener la URL del túnel.${NC}"
    echo -e "   Revisa: $LOG_DIR/cloudflared.log"
    echo -e "   Streamlit sigue activo en: http://localhost:$STREAMLIT_PORT"
fi

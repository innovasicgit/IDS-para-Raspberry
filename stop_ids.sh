#!/bin/bash
# ============================================================
# IDS para Raspberry Pi — Script de parada
# Detiene Streamlit + Cloudflare Tunnel
# ============================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🛑 Deteniendo IDS..."

pkill -f "streamlit run" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null

sleep 1

# Verificar
if pgrep -f "streamlit run" > /dev/null; then
    echo -e "${RED}⚠️  Streamlit sigue corriendo. Forzando...${NC}"
    pkill -9 -f "streamlit run" 2>/dev/null
fi

if pgrep -f "cloudflared tunnel" > /dev/null; then
    echo -e "${RED}⚠️  Tunnel sigue corriendo. Forzando...${NC}"
    pkill -9 -f "cloudflared tunnel" 2>/dev/null
fi

echo -e "${GREEN}✅ IDS detenido completamente.${NC}"

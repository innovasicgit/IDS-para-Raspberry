#!/bin/bash
# Script para detener el Backend API

if [ -f "backend.pid" ]; then
    PID=$(cat backend.pid)
    if ps -p $PID > /dev/null; then
        echo "🛑 Deteniendo backend (PID: $PID)..."
        kill $PID
        rm backend.pid
        echo "✅ Backend detenido"
    else
        echo "⚠️  El proceso no está corriendo"
        rm backend.pid
    fi
else
    echo "⚠️  No se encontró backend.pid"
    echo "Buscando procesos de backend_api.py..."
    pkill -f backend_api.py && echo "✅ Procesos detenidos" || echo "❌ No se encontraron procesos"
fi

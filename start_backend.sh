#!/bin/bash
# Script de inicio rápido para el Backend API
# Uso: ./start_backend.sh

set -e

echo "🚀 Iniciando Backend API para IDS IoT..."

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "backend_api.py" ]; then
    echo -e "${RED}❌ Error: backend_api.py no encontrado${NC}"
    echo "Asegúrate de estar en el directorio del proyecto"
    exit 1
fi

# Verificar que existe el entorno virtual
if [ ! -d "backend_env" ] && [ ! -d "nuevoEntorno" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado${NC}"
    echo "¿Deseas crear uno? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        echo "Creando entorno virtual..."
        python3 -m venv backend_env
        echo -e "${GREEN}✅ Entorno creado${NC}"
    else
        exit 1
    fi
fi

# Activar entorno virtual
if [ -d "backend_env" ]; then
    source backend_env/bin/activate
elif [ -d "nuevoEntorno" ]; then
    source nuevoEntorno/bin/activate
fi

echo -e "${GREEN}✅ Entorno virtual activado${NC}"

# Verificar dependencias
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Instalando dependencias...${NC}"
    pip install -r requirements_backend.txt
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
fi

# Verificar permisos de tshark
if ! groups | grep -q wireshark; then
    echo -e "${YELLOW}⚠️  Tu usuario no está en el grupo 'wireshark'${NC}"
    echo "Ejecuta: sudo usermod -a -G wireshark \$USER"
    echo "Luego cierra sesión y vuelve a entrar"
    echo ""
    echo "¿Continuar de todas formas? (s/n)"
    read -r response
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Verificar que existen los modelos
echo "Verificando modelos ML..."
missing_models=0

for model in "model/iforest__EJERCICIO10_n_components6_fit.pkl" \
             "model/ocsvm__EJERCICIO10_n_components6_fit.pkl" \
             "model/kmeans1__EJERCICIO10_n_components6_over.pkl" \
             "model/autoencoder.pkl" \
             "model/list_kmeans_over.txt"; do
    if [ ! -f "$model" ]; then
        echo -e "${RED}❌ No encontrado: $model${NC}"
        missing_models=1
    fi
done

if [ $missing_models -eq 1 ]; then
    echo -e "${RED}❌ Faltan modelos ML${NC}"
    echo "Asegúrate de tener todos los modelos en la carpeta 'model/'"
    exit 1
fi

echo -e "${GREEN}✅ Todos los modelos encontrados${NC}"

# Obtener IP local
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  Backend API listo para iniciar${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo -e "  Servidor: ${YELLOW}http://0.0.0.0:8000${NC}"
echo -e "  IP Local: ${YELLOW}http://${LOCAL_IP}:8000${NC}"
echo ""
echo -e "  Configura el frontend con:"
echo -e "  ${YELLOW}BACKEND_API_URL=http://${LOCAL_IP}:8000${NC}"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""

# Preguntar si desea ejecutar en background
echo "¿Ejecutar en segundo plano? (s/n)"
read -r background

if [[ "$background" =~ ^[Ss]$ ]]; then
    echo "Iniciando en background..."
    nohup python backend_api.py > backend.log 2>&1 &
    PID=$!
    echo $PID > backend.pid
    echo -e "${GREEN}✅ Backend corriendo en background (PID: $PID)${NC}"
    echo ""
    echo "Para ver logs: tail -f backend.log"
    echo "Para detener: kill \$(cat backend.pid)"
else
    echo "Iniciando en primer plano..."
    echo "Presiona Ctrl+C para detener"
    echo ""
    python backend_api.py
fi
